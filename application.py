from flask import Flask, render_template, request
import sqlite3
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField
import os


# page routes
application = Flask(__name__)
SECRET_KEY = os.urandom(32)
application.config["SECRET_KEY"] = SECRET_KEY


class ContactForm(FlaskForm):
    name = StringField("Name")
    email = StringField("Email")
    subject = StringField("Subject")
    message = TextAreaField("Message")
    submit = SubmitField("Send")


@application.route("/", methods=["POST", "GET"])
def index():
    return render_template("index.html")


@application.route("/resume")
def resume():
    return render_template("resume.html")


@application.route("/projects")
def projects():
    return render_template("projects.html")


@application.route("/contact", methods=["POST", "GET"])
def get_contact():
    form = ContactForm()
    if request.method == "POST":
        name = request.form["name"]
        email = request.form["email"]
        subject = request.form["subject"]
        message = request.form["message"]
        res = (name, email, subject, message)

        con = sqlite3.connect(
            "contactsPage.db"
        )  # create/connect to sqlite db and thene ccreate a cursor to execute cmds
        cur = con.cursor()
        cur.execute(
            """CREATE TABLE IF NOT EXISTS contactsPage
            (name text, email text, subject text, message text)"""
        )
        cur.executemany("INSERT INTO contactsPage VALUES(?,?,?,?)", (res,))
        cur.close()
        con.commit()

        return render_template("ThankYou.html")
    else:
        return render_template("contact.html", form=form)


if __name__ == "__main__":
    application.run(debug=True)
