from flask import Flask, render_template, request, redirect, url_for, make_response
from datetime import datetime
import bleach

app = Flask(__name__)

comments = []
profiles = {}
announcements = []

ALLOWED_TAGS = []  # ou ['b','i','u','a'] si tu veux autoriser quelques balises sûres
ALLOWED_ATTRS = {'a': ['href', 'title']}

def sanitize_text(text):
    # nettoyage: whitelist + suppression des scripts
    return bleach.clean(text, tags=ALLOWED_TAGS, attributes=ALLOWED_ATTRS, strip=True)

@app.after_request
def set_security_headers(response):
    # CSP renforcée : n'autorise que le même domaine (no inline)
    response.headers['Content-Security-Policy'] = "default-src 'self'; script-src 'self'; object-src 'none';"
    response.headers['X-Frame-Options'] = 'DENY'
    response.headers['X-Content-Type-Options'] = 'nosniff'
    return response

@app.route('/')
def home():
    return render_template('base.html')

# ---------- Comments ----------
@app.route('/comments', methods=['GET'])
def comments_page():
    return render_template('comments_secure.html', comments=comments)

@app.route('/comments/post', methods=['POST'])
def post_comment():
    name = request.form.get('name', 'Anonyme')
    text = request.form.get('text', '')
    comments.append({
        'name': sanitize_text(name),
        'text': sanitize_text(text),
        'date': datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')
    })
    return redirect(url_for('comments_page'))

# ---------- Profile ----------
@app.route('/profile/<username>', methods=['GET'])
def profile_page(username):
    bio = profiles.get(username, '')
    return render_template('profile_secure.html', username=username, bio=bio)

@app.route('/profile/<username>/edit', methods=['POST'])
def edit_profile(username):
    bio = request.form.get('bio', '')
    profiles[username] = sanitize_text(bio)
    return redirect(url_for('profile_page', username=username))

# ---------- Announcements ----------
@app.route('/announcements', methods=['GET'])
def announcements_page():
    return render_template('announcements_secure.html', announcements=announcements)

@app.route('/announcements/post', methods=['POST'])
def post_announcement():
    title = request.form.get('title', 'No Title')
    body = request.form.get('body', '')
    announcements.append({
        'title': sanitize_text(title),
        'body': sanitize_text(body),
        'date': datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')
    })
    return redirect(url_for('announcements_page'))

if __name__ == '__main__':
    app.run(debug=False, port=5001)
