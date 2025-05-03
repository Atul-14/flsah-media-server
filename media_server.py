from flask import Flask, render_template, request, redirect, url_for, session, send_from_directory
from dotenv import load_dotenv
import os, json, glob

# Load environment variables from .env
load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY")

# Load users from users.json
with open("users.json") as f:
    USERS = json.load(f)

# Load media folder paths from .env
CATEGORIES = {
    "Movies": os.getenv("MOVIES_PATH"),
    "Series": os.getenv("SERIES_PATH"),
    "Photos": os.getenv("PHOTOS_PATH")
}

# Home page with media listing
@app.route('/')
def index():
    if 'username' not in session:
        return redirect(url_for('login'))

    media = {}
    for category, folder_path in CATEGORIES.items():
        if folder_path and os.path.exists(folder_path):
            # Recursively find all files in subfolders
            files = glob.glob(os.path.join(folder_path, '**', '*.*'), recursive=True)
            media_files = [
                os.path.relpath(f, folder_path)
                for f in files
                if os.path.isfile(f) and f.lower().endswith(('.mp4', '.mkv', '.avi', '.mov', '.jpg', '.jpeg', '.png'))
            ]
            media[category] = media_files
        else:
            media[category] = []

    return render_template('index.html', media=media, username=session['username'])

# Serve media files from actual paths
@app.route('/media/<category>/<path:filepath>')
def serve_media(category, filepath):
    folder = CATEGORIES.get(category)
    if not folder:
        return "Invalid category", 404

    full_path = os.path.join(folder, filepath)

    if not os.path.isfile(full_path):
        return "File not found", 404

    # Serve the file from the correct directory
    directory = os.path.dirname(full_path)
    filename = os.path.basename(full_path)
    return send_from_directory(directory, filename)


# Login page
@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        uname = request.form['username']
        passwd = request.form['password']
        if uname in USERS and USERS[uname] == passwd:
            session['username'] = uname
            return redirect(url_for('index'))
        else:
            error = 'Invalid credentials'
    return render_template('login.html', error=error)

# Logout
@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

# Run server
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
