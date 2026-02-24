#!/usr/bin/env python3
import os
import sys
import subprocess
import glob
import argparse
import json
import logging
from pathlib import Path

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')

def get_env_var(name, default=None):
    # Github Actions inputs are passed as INPUT_<NAME_IN_UPPERCASE>
    env_name = f"INPUT_{name.upper()}"
    return os.environ.get(env_name, os.environ.get(name, default))

def run_command(command, cwd=None, env=None, capture_output=True):
    try:
        logging.info(f"Running: {' '.join(command)}")
        # Use GITHUB_WORKSPACE as default cwd if available, else current directory
        if cwd is None:
             cwd = os.environ.get('GITHUB_WORKSPACE', '.')

        result = subprocess.run(
            command,
            cwd=cwd,
            env=env,
            check=True,
            capture_output=capture_output,
            text=True
        )
        if result.stdout:
            logging.info(result.stdout)
        return True
    except subprocess.CalledProcessError as e:
        logging.error(f"Command failed: {e}")
        if e.stdout:
            logging.info(e.stdout)
        if e.stderr:
            logging.error(e.stderr)
        return False

def get_changed_files(abc_dir):
    """
    Detects changed .abc files in a push event.
    Returns a list of filenames (relative to abc_dir) or None if detection fails/not applicable.
    """
    event_name = os.environ.get('GITHUB_EVENT_NAME')

    if event_name != 'push':
        logging.info(f"Event is {event_name}, not 'push'. Skipping changed file detection.")
        return None

    # Get the commits range
    # In GitHub Actions, payload is at GITHUB_EVENT_PATH
    event_path = os.environ.get('GITHUB_EVENT_PATH')
    if not event_path or not os.path.exists(event_path):
        logging.warning("GITHUB_EVENT_PATH not found.")
        return None

    try:
        with open(event_path, 'r') as f:
            payload = json.load(f)

        before = payload.get('before')
        after = payload.get('after')

        if not before or not after:
            logging.warning("Could not determine commit range from event payload.")
            return None

        # If before is all zeros (new branch), detection might be tricky, usually diff against empty tree or just return None (process all)
        if before == '0000000000000000000000000000000000000000':
             logging.info("New branch detected. Rebuilding all.")
             return None

        logging.info(f"Checking for changes between {before} and {after}")

        # We need to run git diff. The workspace is likely safe, but we might need to config safe.directory
        subprocess.run(['git', 'config', '--global', '--add', 'safe.directory', '*'], check=False)

        # Run git diff
        # We use 'git diff --name-only before after'
        # Ensure we have the history. If shallow, this might fail.
        cmd = ['git', 'diff', '--name-only', before, after]
        # Run inside workspace
        cwd = os.environ.get('GITHUB_WORKSPACE', '.')
        result = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True, check=True)

        changed_files = result.stdout.splitlines()
        abc_files = [f for f in changed_files if f.endswith('.abc')]

        # Filter files that are in abc_dir
        # abc_dir is relative to workspace usually.
        # But changed_files are relative to workspace root.

        # Normalize abc_dir relative to workspace
        # If abc_dir is absolute (starts with /), we assume it's mapped. But git diff returns repo paths.
        # We assume abc_dir is relative to repo root (input 'abcs' -> 'abcs')

        abc_dir_rel = os.path.normpath(abc_dir)
        if os.path.isabs(abc_dir_rel):
            # Try to make it relative to workspace if it starts with workspace
            workspace = os.environ.get('GITHUB_WORKSPACE', '')
            if abc_dir_rel.startswith(workspace):
                abc_dir_rel = os.path.relpath(abc_dir_rel, workspace)
            else:
                 # If absolute and not in workspace, git detection won't match easily unless we know where it maps.
                 # But usually abc_dir is 'abcs'.
                 abc_dir_rel = 'abcs' # Fallback?

        filtered_files = []
        for f in abc_files:
            # f is 'abcs/tune.abc'
            if abc_dir_rel == '.' or f.startswith(abc_dir_rel + os.sep) or f == abc_dir_rel:
                # We want the path relative to abc_dir?
                # The scripts loop over files. generate_mp3.py takes full path. create_pdf.sh takes ABC_FILENAME (no ext) and looks in ABC_DIR.

                # We need to extract filename relative to abc_dir
                if abc_dir_rel == '.':
                     rel_path = f
                else:
                     rel_path = os.path.relpath(f, abc_dir_rel)

                if not rel_path.startswith('..'):
                    filtered_files.append(rel_path)

        logging.info(f"Found changed ABC files: {filtered_files}")
        return filtered_files

    except Exception as e:
        logging.warning(f"Failed to detect changed files: {e}. Falling back to processing all.")
        return None

def main():
    # Load inputs
    action = get_env_var('ACTION', 'all')
    skip_errors = get_env_var('SKIP_ERRORS', 'true').lower() == 'true'
    force_creation = get_env_var('FORCE_CREATION', 'false').lower() == 'true'

    # Directories
    # In action.yml, defaults are 'abcs', 'pdfs', etc.
    # We resolve them to absolute paths for the scripts, assuming they are relative to workspace.
    workspace = os.environ.get('GITHUB_WORKSPACE', os.getcwd())

    def resolve(path):
        if os.path.isabs(path):
            return path
        return os.path.join(workspace, path)

    abc_dir_input = get_env_var('ABC_DIR', 'abcs')
    abc_dir = resolve(abc_dir_input)
    pdf_dir = resolve(get_env_var('PDF_DIR', 'pdfs'))
    mp3_dir = resolve(get_env_var('MP3_DIR', 'mp3s'))
    csv_dir = resolve(get_env_var('CSV_DIR', 'csvs'))

    # Specific file override
    file_name = get_env_var('FILE_NAME')

    # Branch config
    branches_input = get_env_var('BRANCHES', '*')
    current_branch = os.environ.get('GITHUB_REF_NAME', '')

    # Determine files to process
    files_to_process = []

    if file_name:
        logging.info(f"File name explicitly provided: {file_name}. Ignoring change detection.")
        # Ensure it has extension if needed, but file_name input says "without extension" usually?
        # create_pdf.sh expects ABC_FILENAME (no ext).
        # generate_mp3.py expects path to file (with ext).
        # We will normalize to filename with extension for the list.
        if not file_name.endswith('.abc'):
             files_to_process = [f"{file_name}.abc"]
        else:
             files_to_process = [file_name]
    else:
        # Check change detection
        matched = False
        if branches_input.strip() == '*':
            matched = True
        else:
            branches = [b.strip() for b in branches_input.split(',')]
            if current_branch in branches:
                matched = True

        if matched and os.environ.get('GITHUB_EVENT_NAME') == 'push':
            logging.info(f"Branch '{current_branch}' matches config and event is push. Attempting to detect changed files.")
            changed = get_changed_files(abc_dir_input)
            if changed is not None:
                files_to_process = changed
            else:
                # Fallback to all
                files_to_process = glob.glob(os.path.join(abc_dir, '*.abc'))
                files_to_process = [os.path.relpath(f, abc_dir) for f in files_to_process]
        else:
            logging.info("Processing all files (no branch match or not push event).")
            # Glob all .abc files in abc_dir
            if os.path.exists(abc_dir):
                files_to_process = glob.glob(os.path.join(abc_dir, '*.abc'))
                files_to_process = [os.path.relpath(f, abc_dir) for f in files_to_process]
            else:
                logging.error(f"ABC directory {abc_dir} does not exist.")
                sys.exit(1)

    if not files_to_process:
        logging.info("No files to process.")
        return # Success (nothing to do)

    logging.info(f"Files to process: {files_to_process}")

    # Export common env vars for the scripts
    os.environ['ABC_DIR'] = abc_dir
    os.environ['PDF_DIR'] = pdf_dir
    os.environ['MP3_DIR'] = mp3_dir
    os.environ['CSV_DIR'] = csv_dir
    if force_creation:
        os.environ['FORCE_CREATION'] = '1'

    # Ensure output directories exist
    for d in [pdf_dir, mp3_dir, csv_dir]:
        os.makedirs(d, exist_ok=True)

    # 1. Run JPG conversion if needed (global or prereq)
    # convert_jpg_to_eps.sh processes all jpgs in ABC_DIR.
    # It doesn't take file list.
    if action in ['all', 'jpgs', 'pdfs']:
         logging.info("Running JPG to EPS conversion...")
         # convert_jpg_to_eps.sh expects ABC_DIR env var.
         run_command(['/scripts/convert_jpg_to_eps.sh'])

    if action == 'jpgs':
        logging.info("Action is jpgs (conversion only). Done.")
        return

    # 2. Process files
    for f in files_to_process:
        # f is relative to abc_dir, e.g. "tune.abc" or "subdir/tune.abc"
        filename_no_ext = os.path.splitext(f)[0]
        # Ensure we handle subdirectories for output if needed?
        # The scripts usually put output in flat dir or specific structure?
        # create_pdf.sh: mkdir -p "$(dirname "$PDF_DIR/${ABC_FILENAME}_raw.ps")"
        # So it handles subdirs if ABC_FILENAME has subdir.

        abc_file_path = os.path.join(abc_dir, f)

        logging.info(f"Processing {f}...")

        os.environ['ABC_FILENAME'] = filename_no_ext

        success = True

        try:
            if action in ['all', 'pdfs']:
                # Run create_pdf.sh
                if not run_command(['/scripts/create_pdf.sh']):
                    success = False

            if action in ['all', 'mp3s']:
                # Run generate_mp3.py
                # It generates MP3s and deletes MIDI (unless keep-midi set?)
                # User default is MP3s.
                cmd = ['python3', '/scripts/generate_mp3.py', abc_file_path, mp3_dir]
                if not run_command(cmd):
                    success = False

            if action in ['midi']:
                # Run generate_mp3.py with --midi-only
                # Output path: MP3_DIR is passed, but it writes to midi/ inside workspace?
                # generate_mp3.py writes to "midi/" relative to CWD.
                # If we run from workspace, it writes to workspace/midi.
                # If we want it in a specific midi dir, we can't easily control it via generate_mp3.py
                # unless we modify it further. But default behavior is fine.
                cmd = ['python3', '/scripts/generate_mp3.py', abc_file_path, mp3_dir, '--midi-only']
                if not run_command(cmd):
                    success = False

            if action in ['all', 'csvs']:
                 # Run generate_csv.py
                 # generate_csv.py input output
                 # Output file: CSV_DIR/filename.csv
                 # Handle subdirs:
                 csv_output = os.path.join(csv_dir, f"{filename_no_ext}.csv")
                 os.makedirs(os.path.dirname(csv_output), exist_ok=True)

                 cmd = ['python3', '/scripts/generate_csv.py', abc_file_path, csv_output]
                 if not run_command(cmd):
                    success = False

        except Exception as e:
            logging.error(f"Error processing {f}: {e}")
            success = False

        if not success and not skip_errors:
            logging.error("Processing failed and skip_errors is false. Exiting.")
            sys.exit(1)

if __name__ == '__main__':
    main()
