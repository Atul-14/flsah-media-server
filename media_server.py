from flask import Flask, render_template, request, redirect, url_for, session
from dotenv import load_dotenv
import os, json

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY")

# Load users
with open("users.json") as f:
    USERS = json.load(f)

@app.route('/')
def index():
    if 'username' not in session:
        return redirect(url_for('login'))
    return render_template('index.html', username=session['username'])

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

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
