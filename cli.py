import os
import argparse
import requests
import json

def test_gemini_api(api_key, text):
    """
    Tests the Gemini API with the provided API key and text.
    """
    url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent"
    headers = {
        'Content-Type': 'application/json',
        'X-goog-api-key': api_key
    }
    data = {
        "contents": [
            {
                "parts": [
                    {
                        "text": text
                    }
                ]
            }
        ]
    }

    try:
        response = requests.post(url, headers=headers, data=json.dumps(data))
        response.raise_for_status()  # Raise an exception for bad status codes
        return response.json()
    except requests.exceptions.RequestException as e:
        return {"error": str(e)}

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="A command-line tool to test the Gemini API.")
    parser.add_argument("api_key", help="Your Gemini API key.")
    parser.add_argument("text", nargs='?', default="Explain how AI works in a few words", help="The text prompt to send to the API. Defaults to 'Explain how AI works in a few words'.")
    args = parser.parse_args()

    result = test_gemini_api(args.api_key, args.text)
    print(json.dumps(result, indent=2))