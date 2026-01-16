import os
import json
from flask import Flask, render_template, send_from_directory, request, redirect, url_for, flash, session

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
CHALLENGES_DIR = os.path.join(BASE_DIR, "challenges")

app = Flask(__name__)
app.secret_key = "dev-secret-change-me"


def load_challenges():
    challenges = []
    solved_ids = session.get("solved_challenges", [])
    if not os.path.isdir(CHALLENGES_DIR):
        return challenges
    for name in sorted(os.listdir(CHALLENGES_DIR)):
        folder = os.path.join(CHALLENGES_DIR, name)
        if not os.path.isdir(folder):
            continue
        meta_path = os.path.join(folder, "meta.json")
        if not os.path.exists(meta_path):
            continue
        try:
            with open(meta_path, "r", encoding="utf-8") as f:
                meta = json.load(f)
                meta.setdefault("id", name)
                meta["solved"] = (name in solved_ids)
                challenges.append(meta)
        except Exception:
            continue
    return challenges


def get_challenge(ch_id):
    # 1. Try direct match (fastest)
    folder = os.path.join(CHALLENGES_DIR, ch_id)
    if os.path.isdir(folder):
        meta_path = os.path.join(folder, "meta.json")
        if os.path.exists(meta_path):
            try:
                with open(meta_path, "r", encoding="utf-8") as f:
                    meta = json.load(f)
                    # If the ID in the file matches (or isn't set), it's a match
                    if meta.get("id", ch_id) == ch_id:
                        return meta
            except Exception:
                pass

    # 2. Fallback: Search all folders (handles case mismatch or folder name != ID)
    if not os.path.isdir(CHALLENGES_DIR):
        return None
        
    for name in os.listdir(CHALLENGES_DIR):
        folder = os.path.join(CHALLENGES_DIR, name)
        if not os.path.isdir(folder): continue
        
        meta_path = os.path.join(folder, "meta.json")
        if os.path.exists(meta_path):
            try:
                with open(meta_path, "r", encoding="utf-8") as f:
                    meta = json.load(f)
                    if meta.get("id") == ch_id:
                        return meta
            except Exception:
                continue
    return None


@app.route("/")
def index():
    challenges = load_challenges()
    
    # Update solved status based on session
    solved_ids = session.get("solved_challenges", [])
    for c in challenges:
        c["solved"] = (c["id"] in solved_ids)
        
    return render_template("index.html", challenges=challenges)


@app.route("/challenge/<ch_id>")
def challenge(ch_id):
    meta = get_challenge(ch_id)
    if not meta:
        flash("Challenge introuvable.", "danger")
        return redirect(url_for("index"))
    
    solved_ids = session.get("solved_challenges", [])
    meta["solved"] = (ch_id in solved_ids)

    files = []
    # Find the actual folder name for this challenge ID
    folder_name = ch_id # Default
    for name in os.listdir(CHALLENGES_DIR):
        try:
            with open(os.path.join(CHALLENGES_DIR, name, "meta.json"), "r", encoding="utf-8") as f:
                if json.load(f).get("id") == ch_id:
                    folder_name = name
                    break
        except:
            continue
            
    folder = os.path.join(CHALLENGES_DIR, folder_name)
    if os.path.isdir(folder):
        for f in sorted(os.listdir(folder)):
            if f == "meta.json":
                continue
            files.append(f)
            
    return render_template("challenge.html", meta=meta, files=files)


@app.route("/download/<ch_id>/<path:filename>")
def download(ch_id, filename):
    # Find the actual folder name for this challenge ID
    folder_name = ch_id # Default
    if os.path.isdir(CHALLENGES_DIR):
        for name in os.listdir(CHALLENGES_DIR):
            try:
                with open(os.path.join(CHALLENGES_DIR, name, "meta.json"), "r", encoding="utf-8") as f:
                    if json.load(f).get("id") == ch_id:
                        folder_name = name
                        break
            except:
                continue

    folder = os.path.join(CHALLENGES_DIR, folder_name)
    return send_from_directory(folder, filename, as_attachment=True)


@app.route("/submit/<ch_id>", methods=["POST"])
def submit(ch_id):
    meta = get_challenge(ch_id)
    if not meta:
        flash("Challenge introuvable.", "danger")
        return redirect(url_for("index"))
    flag = request.form.get("flag", "").strip()
    correct = meta.get("flag", "")
    if flag == "":
        flash("Veuillez entrer un drapeau (flag).", "warning")
    elif flag == correct:
        flash("Bravo ! Drapeau correct. (+{} pts)".format(meta.get("points", 0)), "success")
        
        # Mark as solved in session
        solved_ids = session.get("solved_challenges", [])
        if ch_id not in solved_ids:
            solved_ids.append(ch_id)
            session["solved_challenges"] = solved_ids
            session.modified = True
            
    else:
        flash("Drapeau incorrect. Réessayez.", "danger")
    return redirect(url_for("challenge", ch_id=ch_id))


@app.route("/archives")
def archives():
    return render_template("archives.html") 


@app.route("/operator")
def operator():
    return render_template("operator.html")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
