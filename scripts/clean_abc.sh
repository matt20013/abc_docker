#!/bin/bash
if [ -z "$1" ]; then
    echo "Usage: ./clean_abc.sh <path_to_abc_file>"; exit 1
fi
FILE="$1"
echo "Cleaning up $FILE..."
sed -i 's/\r$//' "$FILE"
sed -i 's/[[:space:]]*$//' "$FILE"
echo "Cleanup complete!"
