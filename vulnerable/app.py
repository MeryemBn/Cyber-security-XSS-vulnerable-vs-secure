from flask import Flask, render_template, request, redirect, url_for, jsonify
from datetime import datetime
import bleach   # <— ajoute cette ligne

app = Flask(__name__)

# stockage en mémoire (demo) : reset à chaque restart - OK pour projet
comments = []
profiles = {}  # key=username -> bio
announcements = []


@app.route('/')
def home():
    return render_template('base.html')


# ---------- Comments (mini-blog) ----------
@app.route('/comments', methods=['GET'])
def comments_page():
    return render_template('comments.html', comments=comments)


@app.route('/comments/post', methods=['POST'])
def post_comment():
    name = request.form.get('name', 'Anonyme')
    text = request.form.get('text', '')
    comments.append({
        'name': name,
        'text': text,
        'date': datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')
    })
    return redirect(url_for('comments_page'))


# ---------- Profile (user bio) ----------
@app.route('/profile/<username>', methods=['GET'])
def profile_page(username):
    bio = profiles.get(username, '')
    return render_template('profile.html', username=username, bio=bio)


@app.route('/profile/<username>/edit', methods=['POST'])
def edit_profile(username):
    bio = request.form.get('bio', '')
    profiles[username] = bio
    return redirect(url_for('profile_page', username=username))


# ---------- Announcements (admin-like WYSIWYG) ----------
@app.route('/announcements', methods=['GET'])
def announcements_page():
    return render_template('announcements.html', announcements=announcements)


@app.route('/announcements/post', methods=['POST'])
def post_announcement():
    title = request.form.get('title', 'No Title')
    body = request.form.get('body', '')
    announcements.append({
        'title': title,
        'body': body,
        'date': datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')
    })
    return redirect(url_for('announcements_page'))


# ---------- ADMIN UTILITIES ----------
@app.route('/admin/clear_comments', methods=['POST'])
def admin_clear_comments():
    """Vide complètement la liste des commentaires (RESET complet)."""
    global comments
    comments = []
    return jsonify({"status": "ok", "message": "Tous les commentaires ont été supprimés"}), 200


@app.route('/admin/delete_comment/<int:idx>', methods=['POST'])
def admin_delete_comment(idx):
    """Supprime un commentaire par son index dans la liste."""
    try:
        removed = comments.pop(idx)
        return jsonify({"status": "ok", "removed": removed}), 200
    except IndexError:
        return jsonify({"status": "error", "message": "Index invalide"}), 400


@app.route('/admin/sanitize_comments', methods=['POST'])
def admin_sanitize_comments():
    """Nettoie les commentaires existants avec bleach (supprime scripts dangereux)."""
    global comments
    cleaned = []
    for c in comments:
        safe_text = bleach.clean(c.get('text', ''), tags=[], attributes={}, strip=True)
        safe_name = bleach.clean(c.get('name', ''), tags=[], attributes={}, strip=True)
        cleaned.append({
            'name': safe_name,
            'text': safe_text,
            'date': c.get('date')
        })
    comments = cleaned
    return jsonify({
        "status": "ok",
        "message": "Tous les commentaires ont été nettoyés",
        "count": len(comments)
    }), 200


if __name__ == '__main__':
    app.run(debug=True, port=5000)
