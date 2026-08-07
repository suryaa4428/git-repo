from werkzeug.utils import secure_filename
import os
from flask import Flask, request, redirect, render_template, session
import mysql.connector
import bcrypt

app = Flask(__name__)
UPLOAD_FOLDER = os.path.join(app.root_path, "static", "uploads")
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "gif", "pdf"}

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
print("UPLOAD_FOLDER =", app.config["UPLOAD_FOLDER"])
app.secret_key = os.environ.get("SECRET_KEY", "cloudnotes_secret_key")


def get_db():
    return mysql.connector.connect(
        host=os.environ.get("MYSQLHOST"),
        user=os.environ.get("MYSQLUSER"),
        password=os.environ.get("MYSQLPASSWORD"),
        database=os.environ.get("MYSQLDATABASE"),
        port=int(os.environ.get("MYSQLPORT", 3306))
    )


def allowed_file(filename):
    return (
        "." in filename
        and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS
    )


def get_user_theme(cursor, user_id):
    """Fetch the current theme for a user, defaulting to 'light' if unset."""
    cursor.execute(
        "SELECT theme FROM users WHERE id=%s",
        (user_id,)
    )
    row = cursor.fetchone()
    theme = row[0] if row else None
    return theme if theme else "light"


@app.route("/")
def index():
    if "user_id" not in session:
        return redirect("/login")

    db = get_db()
    cursor = db.cursor()

    theme = get_user_theme(cursor, session["user_id"])

    cursor.execute(
        "SELECT * FROM notes WHERE user_id=%s AND deleted=FALSE ORDER BY favorite DESC, pinned DESC, created_at DESC",
        (session["user_id"],)
    )
    notes = cursor.fetchall()

    cursor.close()
    db.close()

    return render_template(
        "index.html",
        notes=notes,
        theme=theme
    )


@app.route("/add", methods=["POST"])
def add_note_submit():

    if "user_id" not in session:
        return redirect("/login")

    title = request.form.get("title", "")
    note = request.form.get("note", "")
    category = request.form.get("category", "General")

    if note.strip() == "":
        return redirect("/")

    filename = None

    if "file" in request.files:
        file = request.files["file"]

        if file and file.filename != "" and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(
                os.path.join(
                    app.config["UPLOAD_FOLDER"],
                    filename
                )
            )

    db = get_db()
    cursor = db.cursor()

    try:
        user_id = session["user_id"]

        cursor.execute(
            """
            INSERT INTO notes
            (title, note, category, filename, user_id)
            VALUES (%s, %s, %s, %s, %s)
            """,
            (title, note, category, filename, user_id)
        )

        db.commit()

    finally:
        cursor.close()
        db.close()

    return redirect("/")


@app.route("/delete/<int:id>", methods=["POST"])
def delete_note(id):

    if "user_id" not in session:
        return redirect("/login")

    db = get_db()
    cursor = db.cursor()

    try:

        cursor.execute(
            """
            UPDATE notes
            SET deleted = TRUE
            WHERE id = %s
            AND user_id = %s
            """,
            (id, session["user_id"])
        )

        db.commit()

    finally:

        cursor.close()
        db.close()

    return redirect("/")


@app.route("/pin/<int:id>", methods=["POST"])
def pin(id):
    if "user_id" not in session:
        return redirect("/login")

    db = get_db()
    cursor = db.cursor()
    try:
        cursor.execute(
            "SELECT pinned FROM notes WHERE id=%s AND user_id=%s",
            (id, session["user_id"])
        )
        note = cursor.fetchone()

        if note:
            new_value = not note[0]
            cursor.execute(
                "UPDATE notes SET pinned=%s WHERE id=%s AND user_id=%s",
                (new_value, id, session["user_id"])
            )
            db.commit()
    finally:
        cursor.close()
        db.close()

    return redirect("/")


@app.route("/edit/<int:id>", methods=["POST"])
def edit_note(id):
    if "user_id" not in session:
        return redirect("/login")

    title = request.form["title"]
    note = request.form["note"]
    category = request.form["category"]

    db = get_db()
    cursor = db.cursor()

    try:
        cursor.execute(
            """
            UPDATE notes
            SET title=%s,
                note=%s,
                category=%s
            WHERE id=%s
            AND user_id=%s
            """,
            (title, note, category, id, session["user_id"])
        )
        db.commit()
    finally:
        cursor.close()
        db.close()

    return redirect("/")


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")

        if not username or not password:
            return render_template("register.html", error="Username and password are required")

        hashed_pw = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())

        db = get_db()
        cursor = db.cursor()
        try:
            cursor.execute(
                "INSERT INTO users (username, password) VALUES (%s, %s)",
                (username, hashed_pw.decode("utf-8"))
            )
            db.commit()
        except mysql.connector.errors.IntegrityError:
            return render_template("register.html", error="Username already taken")
        finally:
            cursor.close()
            db.close()

        return redirect("/login")

    return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")

        db = get_db()
        cursor = db.cursor()
        try:
            cursor.execute(
                "SELECT * FROM users WHERE username=%s",
                (username,)
            )
            user = cursor.fetchone()

            if user and bcrypt.checkpw(
                password.encode("utf-8"),
                user[2].encode("utf-8")
            ):
                session["user_id"] = user[0]
                return redirect("/")
        finally:
            cursor.close()
            db.close()

        return render_template("login.html", error="Invalid username or password")

    return render_template("login.html")


@app.route("/logout")
def logout():
    session.clear()
    return redirect("/login")


@app.route("/test")
def test():
    return str(session.get("user_id"))


@app.route("/change_password", methods=["GET", "POST"])
def change_password():

    if "user_id" not in session:
        return redirect("/login")

    db = get_db()
    cursor = db.cursor()

    if request.method == "POST":

        old_password = request.form["old_password"]
        new_password = request.form["new_password"]

        cursor.execute(
            "SELECT password FROM users WHERE id=%s",
            (session["user_id"],)
        )

        row = cursor.fetchone()
        if row is None:
            cursor.close()
            db.close()
            return redirect("/login")

        stored_password = row[0]

        if bcrypt.checkpw(
            old_password.encode("utf-8"),
            stored_password.encode("utf-8")
        ):
            new_hash = bcrypt.hashpw(
                new_password.encode("utf-8"),
                bcrypt.gensalt()
            ).decode("utf-8")

            cursor.execute(
                "UPDATE users SET password=%s WHERE id=%s",
                (new_hash, session["user_id"])
            )
            db.commit()

            cursor.close()
            db.close()
            return redirect("/account?success=1")
        else:
            cursor.close()
            db.close()
            return redirect("/change_password?error=wrong_password")

    theme = get_user_theme(cursor, session["user_id"])
    cursor.close()
    db.close()

    return render_template("change_password.html", theme=theme)


@app.route("/profile")
def profile():

    if "user_id" not in session:
        return redirect("/login")

    db = get_db()
    cursor = db.cursor()

    user_id = session["user_id"]

    theme = get_user_theme(cursor, user_id)

    cursor.execute(
        "SELECT * FROM users WHERE id=%s",
        (user_id,)
    )
    user = cursor.fetchone()

    cursor.execute(
        "SELECT COUNT(*) FROM notes WHERE user_id=%s",
        (user_id,)
    )
    total_notes = cursor.fetchone()[0]

    cursor.execute(
        "SELECT COUNT(*) FROM notes WHERE user_id=%s AND pinned=1",
        (user_id,)
    )
    pinned_notes = cursor.fetchone()[0]

    cursor.close()
    db.close()

    return render_template(
        "profile.html",
        user=user,
        total_notes=total_notes,
        pinned_notes=pinned_notes,
        theme=theme
    )


@app.route("/trash")
def trash():

    if "user_id" not in session:
        return redirect("/login")

    db = get_db()
    cursor = db.cursor()

    try:

        theme = get_user_theme(cursor, session["user_id"])

        cursor.execute(
            """
            SELECT id, note, created_at, user_id,
                   title, pinned, category,
                   filename, favorite
            FROM notes
            WHERE user_id=%s
            AND deleted=TRUE
            ORDER BY created_at DESC
            """,
            (session["user_id"],)
        )

        notes = cursor.fetchall()

    finally:

        cursor.close()
        db.close()

    return render_template("trash.html", notes=notes, theme=theme)


@app.route("/toggle_theme")
def toggle_theme():

    if "user_id" not in session:
        return redirect("/login")

    db = get_db()
    cursor = db.cursor()

    try:

        current_theme = get_user_theme(cursor, session["user_id"])

        if current_theme == "dark":
            new_theme = "light"
        else:
            new_theme = "dark"

        cursor.execute(
            "UPDATE users SET theme=%s WHERE id=%s",
            (new_theme, session["user_id"])
        )

        db.commit()

    finally:

        cursor.close()
        db.close()

    return redirect("/")


@app.route("/restore/<int:id>", methods=["POST"])
def restore(id):

    if "user_id" not in session:
        return redirect("/login")

    db = get_db()
    cursor = db.cursor()

    try:

        cursor.execute(
            """
            UPDATE notes
            SET deleted = FALSE
            WHERE id = %s
            AND user_id = %s
            """,
            (id, session["user_id"])
        )

        db.commit()

    finally:

        cursor.close()
        db.close()

    return redirect("/trash")


@app.route("/delete_forever/<int:id>", methods=["POST"])
def delete_forever(id):

    if "user_id" not in session:
        return redirect("/login")

    db = get_db()
    cursor = db.cursor()

    try:

        cursor.execute(
            """
            DELETE FROM notes
            WHERE id = %s
            AND user_id = %s
            """,
            (id, session["user_id"])
        )

        db.commit()

    finally:

        cursor.close()
        db.close()

    return redirect("/trash")


@app.route("/favorite/<int:id>", methods=["POST"])
def favorite(id):
    if "user_id" not in session:
        return redirect("/login")

    db = get_db()
    cursor = db.cursor()

    try:
        cursor.execute(
            "SELECT favorite FROM notes WHERE id=%s AND user_id=%s",
            (id, session["user_id"])
        )

        note = cursor.fetchone()

        if note:
            cursor.execute(
                "UPDATE notes SET favorite=%s WHERE id=%s AND user_id=%s",
                (not note[0], id, session["user_id"])
            )
            db.commit()

    finally:
        cursor.close()
        db.close()

    return redirect("/")


import os

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
