#!/bin/bash

# Check for -h or --help
if [[ "$1" == "-h" || "$1" == "--help" ]]; then
    echo "Usage: ./run_cli.sh [API_KEY]"
    echo
    echo "Arguments:"
    echo "  API_KEY   Your Gemini API key."
    exit 0
fi

# Check if API key is provided
if [ -z "$1" ]; then
    read -p "Enter your Gemini API key: " api_key
else
    api_key=$1
fi

curl "https://generativelanguage.googleapis.com/v1beta/models/" \
  -H 'Content-Type: application/json' \
  -H "X-goog-api-key: $api_key" \
  -X GET\
