#!/bin/bash

# Check for -h or --help
if [[ "$1" == "-h" || "$1" == "--help" ]]; then
    echo "Usage: ./run_cli.sh [API_KEY] [PROMPT]"
    echo
    echo "Arguments:"
    echo "  API_KEY   Your Gemini API key."
    echo "  PROMPT    The prompt to send to the API. Defaults to 'Explain how AI works in a few words'."
    exit 0
fi

# Check if API key is provided
if [ -z "$1" ]; then
    read -p "Enter your Gemini API key: " api_key
else
    api_key=$1
fi

# Check if prompt is provided
if [ -z "$2" ]; then
    read -p "Enter your prompt (or press Enter for default): " prompt
    if [ -z "$prompt" ]; then
        prompt="Explain how AI works in a few words"
    fi
else
    prompt=$2
fi

curl "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent" \
  -H 'Content-Type: application/json' \
  -H "X-goog-api-key: $api_key" \
  -X POST \
  -d "{
    \"contents\": [
      {
        \"parts\": [
          {
            \"text\": \"$prompt\"
          }
        ]
      }
    ]
  }"