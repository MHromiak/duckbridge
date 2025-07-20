#!/bin/bash
# run_args.sh

# Usage: ./run_args.sh /path/to/file.txt "Bearer your_token_123"

if [ "$#" -ne 2 ]; then
  echo "Usage: $0 <filepath> <auth_string>"
  exit 1
fi

FILEPATH="$1"
AUTH="$2"

python cli_input.py -f "$FILEPATH" -a "$AUTH"
