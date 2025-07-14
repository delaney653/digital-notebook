"""Used to render the 'Choose your color!' application"""

import time
import os
from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import OperationalError


app = Flask(__name__)

if os.getenv("ENV") == "testing":
    app.config["SQLALCHEMY_DATABASE_URI"] = (
        "mysql+pymysql://root:password@mysql-test/test_notes"
    )
else:
    app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://root:password@mysql/notes"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app) 


class Note(db.Model):
    """Used to create a table that has 2 columns: an id as a primary key, and
    the name of the color chosen."""

    __tablename__ = "notes"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(10000))


def add_color(color_name):
    """Add a color to the database"""
    new_note = Note(name=color_name)
    db.session.add(new_note)
    db.session.commit()


@app.route("/", methods=["GET", "POST"])
def home():
    """Renders home page based on what colors have been previously selected"""
    notes = Note.query.all()
    # Color options -- default color = #AntiqueWhite
    color_options = ["Crimson", "LightBlue", "Plum", "LightSeaGreen", "Ivory"]
    selected_color = None
    feedback = []
    non_red_count = 0
    for note in notes:
        color = note.name.lower()
        if color == "crimson":
            feedback.append("You've chosen the best color. I vote we stick with this color!")
        else:
            non_red_count += 1
            if non_red_count == 1:
                feedback.append(
                    "Hmm, you chose an ugly color… Try a different one for my sake."
                )
            elif non_red_count == 2:
                feedback.append("Better than the last one, but try a different color.")
            elif non_red_count >= 3:
                feedback.append(
                    "You're not very good at this... Please just stick to crimson."
                )

    combined = list(zip(notes, feedback))
    selected_color = notes[-1].name if notes else "AntiqueWhite"
    return render_template(
        "index.html",
        color_options=color_options,
        color_feedback=combined,
        selected_color=selected_color,
    )


@app.route("/add", methods=["GET", "POST"])
def add():
    """Adds a color to the database"""
    color_name = request.form.get("note")
    add_color(color_name=color_name)
    return redirect("/")


@app.route("/delete/<int:id>", methods=["GET", "POST"])
def delete(id):
    """Deletes a color from the stored colors"""
    color = Note.query.get(id)
    db.session.delete(color)
    db.session.commit()
    return redirect("/")


@app.route("/reset", methods=["GET", "POST"])
def reset_color():
    """Clears out database of all previously selected colors"""
    Note.query.delete()
    db.session.commit()
    return redirect("/")


if __name__ == "__main__":
    with app.app_context():
        for _ in range(5):
            try:
                db.create_all()
                break
            except OperationalError:
                print("Database not ready, retrying in 2s...")
                time.sleep(2)
        else:
            print("Could not connect to database after 5 tries. Exiting.")
            exit(1)

    app.run(host="0.0.0.0", port=5000, debug=True)
