import requests
import json
from flask import Flask, g, render_template, request, jsonify, redirect
import sqlite3
import datetime
import os

app = Flask(__name__)
DATABASE = 'database.db'

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
        db.row_factory = sqlite3.Row
    return db

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

def init_db():
    """Initializes the database."""
    db = get_db()
    db.execute(
        'CREATE TABLE IF NOT EXISTS api_keys ('
        ' id INTEGER PRIMARY KEY AUTOINCREMENT,'
        ' name TEXT,'
        ' key TEXT NOT NULL UNIQUE,'
        ' status TEXT NOT NULL,'
        ' last_checked TEXT NOT NULL'
        ')'
    )
    db.commit()

@app.cli.command('init-db')
def init_db_command():
    """Clear the existing data and create new tables."""
    init_db()
    print('Initialized the database.')

def initialize_database():
    """Initializes the database and table if they do not exist."""
    with app.app_context():
        db = get_db()
        cursor = db.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='api_keys'")
        if cursor.fetchone() is None:
            init_db()
            print('Initialized the database.')

@app.before_request
def before_request():
    """Create the database and table if they don't exist."""
    initialize_database()

@app.route('/', methods=['GET', 'POST'])
def index():
    page = request.args.get('page', 1, type=int)
    search = request.args.get('search', '', type=str)
    page_size = 5  # Number of keys per page

    if request.method == 'POST':
        api_key = request.form.get('api_key')
    else:  # GET request
        api_key = request.args.get('api_key')

    result = {}
    if api_key:
        api_url = "https://generativelanguage.googleapis.com/v1beta/models/"
        headers = {
            "Content-Type": "application/json",
            "X-goog-api-key": api_key
        }

        try:
            response = requests.get(api_url, headers=headers)
            response_data = response.json()

            status = "unknown"
            message = "API call successful"

            if response.status_code == 200:
                status = "valid"
                message = "API key is valid and request was successful."
            elif response.status_code == 400:
                # Check for specific error messages in the response
                if 'error' in response_data and 'message' in response_data['error']:
                    if "API key expired" in response_data['error']['message']:
                        status = "expired"
                        message = "The API key has expired."
                    else:
                        status = "invalid_format"
                        message = response_data['error']['message']
                else:
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

            db = get_db()
            now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            # Check if the key exists in the database
            existing_key = db.execute('SELECT id FROM api_keys WHERE key = ?', (api_key,)).fetchone()

            if existing_key:
                # If it exists, always update it
                db.execute(
                    'UPDATE api_keys SET status = ?, last_checked = ? WHERE key = ?',
                    (status, now, api_key)
                )
                db.commit()
            elif request.form.get('save_key'):
                # If it's a new key, only save it if the checkbox is checked
                name = request.form.get('key_name')
                if not name:
                    # Generate a default name
                    count = db.execute('SELECT COUNT(id) FROM api_keys').fetchone()[0]
                    name = f"Key #{count + 1}"
                # Validate API key format
                if not (api_key.startswith('AIza') and len(api_key) == 39):
                    print("Invalid API key format. Key not saved.")
                else:
                    db.execute(
                        'INSERT INTO api_keys (name, key, status, last_checked) VALUES (?, ?, ?, ?)',
                        (name, api_key, status, now)
                    )
                    db.commit()


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
    
    db = get_db()
    
    # Apply search filter
    if search:
        query = 'SELECT * FROM api_keys WHERE name LIKE ? OR key LIKE ? ORDER BY last_checked DESC'
        params = ('%' + search + '%', '%' + search + '%')
        total_keys = db.execute('SELECT COUNT(id) FROM api_keys WHERE name LIKE ? OR key LIKE ?', params).fetchone()[0]
    else:
        query = 'SELECT * FROM api_keys ORDER BY last_checked DESC'
        params = ()
        total_keys = db.execute('SELECT COUNT(id) FROM api_keys').fetchone()[0]

    # Apply pagination
    offset = (page - 1) * page_size
    query += ' LIMIT ? OFFSET ?'
    params = params + (page_size, offset)

    keys = db.execute(query, params).fetchall()

    return render_template('api_test.html', result=result, keys=keys, page=page, page_size=page_size, total_keys=total_keys, search=search, api_key=api_key)

@app.route('/delete_key/<int:key_id>', methods=['POST'])
def delete_key(key_id):
    db = get_db()
    db.execute('DELETE FROM api_keys WHERE id = ?', (key_id,))
    db.commit()
    return redirect('/')

@app.route('/update_key/<int:key_id>', methods=['POST'])
def update_key(key_id):
    db = get_db()
    new_api_key = request.form.get('new_api_key')

    # Get the old API key from the database
    old_api_key = db.execute('SELECT key FROM api_keys WHERE id = ?', (key_id,)).fetchone()['key']

    if new_api_key == old_api_key:
        # If the new API key is the same as the old one, return an error message
        return "Error: New API key cannot be the same as the old one."
    else:
        # If the new API key is different from the old one, update the API key in the database
        db.execute('UPDATE api_keys SET key = ? WHERE id = ?', (new_api_key, key_id))
        db.commit()
        return redirect('/')

if __name__ == '__main__':
    app.run(debug=True, port=5001)
