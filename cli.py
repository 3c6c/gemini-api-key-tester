import os
import argparse
import requests
import json

def test_gemini_api(api_key):
    """
    Tests the Gemini API with the provided API key.
    """
    url = "https://generativelanguage.googleapis.com/v1beta/models/"
    headers = {
        'Content-Type': 'application/json',
        'X-goog-api-key': api_key
    }
    
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Raise an exception for bad status codes
        return response.json()
    except requests.exceptions.RequestException as e:
        return {"error": str(e)}

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="A command-line tool to test the Gemini API.")
    parser.add_argument("api_key", help="Your Gemini API key.")
    args = parser.parse_args()

    result = test_gemini_api(args.api_key)
    print(json.dumps(result, indent=2))
