#!/usr/bin/env bash

usage() {
    echo "Usage: $0 [API_KEY] | -f FILE"
    echo
    echo "Arguments:"
    echo "  API_KEY   Your Gemini API key."
    echo "  -f FILE   File containing lines in the format 'owner:api_key' to check multiple keys." 
    exit 0
}

# Check for -h or --help
if [[ "$1" == "-h" || "$1" == "--help" ]]; then
    usage
fi

file=""
api_key=""

# Parse arguments
while [[ $# -gt 0 ]]; do
    case "$1" in
        -h|--help)
            usage
            ;;
        -f|--file)
            file="$2"
            shift 2
            ;;
        *)
            if [ -z "$api_key" ]; then
                api_key="$1"
            fi
            shift
            ;;
    esac
done

check_key() {
    local owner="$1"
    local key="$2"

    echo "--------------------------------------------------"
    if [ -n "$owner" ]; then
        echo "Checking owner: $owner"
    else
        echo "Checking API key"
    fi

    curl "https://generativelanguage.googleapis.com/v1beta/models/" \
      -H 'Content-Type: application/json' \
      -H "X-goog-api-key: $key" \
      -X GET \
      -s

    echo
}

if [ -n "$file" ]; then
    if [ ! -f "$file" ]; then
        echo "File not found: $file"
        exit 1
    fi

    while IFS= read -r line || [ -n "$line" ]; do
        # skip empty lines and comments
        [[ -z "${line// }" ]] && continue
        [[ "$line" =~ ^[[:space:]]*# ]] && continue

        # split at first colon: owner:api_key
        owner="${line%%:*}"
        key="${line#*:}"

        # trim whitespace
        owner="$(echo "$owner" | xargs)"
        key="$(echo "$key" | xargs)"

        if [ -z "$key" ]; then
            echo "Skipping invalid line (no key found): $line"
            continue
        fi

        check_key "$owner" "$key"
    done < "$file"

    exit 0
fi

# If no file provided, fall back to single-key behavior
if [ -z "$api_key" ]; then
    read -p "Enter your Gemini API key: " api_key
fi

check_key "" "$api_key"
