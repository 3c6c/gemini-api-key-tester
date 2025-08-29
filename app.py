import requests
import json
from flask import Flask, g, render_template, request, jsonify
import sqlite3

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def test_api_key():
    if request.method == 'POST':
        api_key = request.form.get('api_key')
        prompt = request.form.get('prompt', 'Explain how AI works in a few words')
    else: # GET request
        api_key = request.args.get('api_key')
        prompt = request.args.get('prompt', 'Explain how AI works in a few words')

    result = {}
    if api_key:
        api_url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent"
        headers = {
            "Content-Type": "application/json",
            "X-goog-api-key": api_key
        }
        payload = {
            "contents": [
                {
                    "parts": [
                        {
                            "text": prompt
                        }
                    ]
                }
            ]
        }

        try:
            response = requests.post(api_url, headers=headers, json=payload)
            response_data = response.json()

            status = "unknown"
            message = "API call successful"

            if response.status_code == 200:
                status = "valid"
                message = "API key is valid and request was successful."
            elif response.status_code == 400:
                status = "invalid_format"
                message = "Bad request. Check API key format or payload."
            elif response.status_code == 403:
                status = "invalid_key_or_permission"
                message = "Forbidden. API key may be invalid or lack permissions."
            elif response.status_code == 429:
                status = "rate_limited"
                message = "Rate limit exceeded. Please try again later."
            else:
                status = "error"
                message = f"An unexpected error occurred: {response.status_code}"

            result = {
                "status": status,
                "message": message,
                "api_response": response_data
            }

        except requests.exceptions.RequestException as e:
            result = {
                "status": "error",
                "message": f"Request failed: {str(e)}",
                "api_response": None
            }
        except json.JSONDecodeError:
            result = {
                "status": "error",
                "message": "Failed to decode API response",
                "api_response": None
            }
            
    return render_template('api_test.html', result=result)

if __name__ == '__main__':
    app.run(debug=True)