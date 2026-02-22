#!/bin/bash
set -e

# Default to current directory if not set (for Github Actions workspace)
WORKSPACE="${GITHUB_WORKSPACE:-.}"

# Resolve absolute paths
# If paths are relative, prepend workspace.
resolve_path() {
    local p="$1"
    if [[ "$p" != /* ]]; then
        echo "$WORKSPACE/$p"
    else
        echo "$p"
    fi
}

export ABC_DIR=$(resolve_path "${INPUT_ABC_DIR:-abcs}")
export PDF_DIR=$(resolve_path "${INPUT_PDF_DIR:-pdfs}")
export MP3_DIR=$(resolve_path "${INPUT_MP3_DIR:-mp3s}")
export CSV_DIR=$(resolve_path "${INPUT_CSV_DIR:-csvs}")

echo "Processing ABC files in: $ABC_DIR"
echo "Outputting PDFs to: $PDF_DIR"
echo "Outputting MP3s to: $MP3_DIR"
echo "Outputting CSVs to: $CSV_DIR"

mkdir -p "$PDF_DIR"
mkdir -p "$MP3_DIR"
mkdir -p "$CSV_DIR"

# Ensure /scripts is in path or we call them directly
cd /scripts

# Run conversions
# Note: convert_jpg_to_eps.sh modifies files in ABC_DIR.
./convert_jpg_to_eps.sh
./create_all_pdfs.sh
./generate_all_mp3s.sh
./generate_all_csvs.sh
