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

# Match Action inputs
# inputs:
#   abc_dir (default 'abcs')
#   file_name (required)

export ABC_DIR=$(resolve_path "${INPUT_ABC_DIR:-abcs}")
export PDF_DIR=$(resolve_path "${INPUT_PDF_DIR:-pdfs}")
export MP3_DIR=$(resolve_path "${INPUT_MP3_DIR:-mp3s}")
export CSV_DIR=$(resolve_path "${INPUT_CSV_DIR:-csvs}")

# Backward compatibility for batch processing if FILE_NAME is not set (though required in action.yml)
ABC_FILENAME="${INPUT_FILE_NAME}"

echo "Processing ABC files in: $ABC_DIR"
echo "Outputting PDFs to: $PDF_DIR"
echo "Outputting MP3s to: $MP3_DIR"
echo "Outputting CSVs to: $CSV_DIR"

mkdir -p "$PDF_DIR"
mkdir -p "$MP3_DIR"
mkdir -p "$CSV_DIR"

# Ensure /scripts is in path or we call them directly
cd /scripts

# If filename is provided, process single file
if [[ -n "$ABC_FILENAME" ]]; then
    echo "Processing single file: $ABC_FILENAME"
    export ABC_FILENAME
    export ABC_FILE="${ABC_FILENAME}.abc"
    export ABC_PATH="$ABC_DIR/$ABC_FILE"

    if [[ ! -f "$ABC_PATH" ]]; then
        echo "Error: File $ABC_PATH not found."
        exit 1
    fi

    # Convert JPG to EPS specifically for this file?
    # Or just run convert_jpg_to_eps.sh for the directory (it's fast if no jpgs)
    ./convert_jpg_to_eps.sh

    # Create PDF
    ./create_pdf.sh

    # Generate MP3
    python3 generate_mp3.py "$ABC_PATH" "$MP3_DIR"

    # Generate CSV (optional but good for completeness)
    python3 generate_csv.py "$ABC_PATH" "$CSV_DIR/${ABC_FILENAME}.csv"

else
    echo "No file_name provided. Running batch processing..."
    # Run conversions
    ./convert_jpg_to_eps.sh
    ./create_all_pdfs.sh
    ./generate_all_mp3s.sh
    ./generate_all_csvs.sh
fi
