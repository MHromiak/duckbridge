import argparse
import os
import sys

def main():
    parser = argparse.ArgumentParser(description="Process file path and auth string.")
    parser.add_argument("--filepath", "-f", type=str, required= True, help="Path to the database")
    parser.add_argument("--auth", "-a", type=str, required=True, help="Authorization string")

    args = parser.parse_args()

    # Validate file path
    if not os.path.isfile(args.filepath):
        print(f"Error: File '{args.filepath}' does not exist.", file=sys.stderr)
        sys.exit(1)

    print(f"File path: {args.filepath}")
    print(f"Auth string: {args.auth}")

if __name__ == "__main__":
    main()