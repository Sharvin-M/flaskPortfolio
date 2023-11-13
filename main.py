from flask import Flask, render_template, url_for, request, redirect, g

# from flask_mail import Mail, Message
from flask_mail import Mail, Message
from flask_sqlalchemy import SQLAlchemy
import sqlite3
from flask_wtf import FlaskForm
from flask_wtf.csrf import CSRFProtect
from wtforms import StringField, BooleanField, TextAreaField, SubmitField
import pandas as pd
import os
import smtplib


# page routes
app = Flask(__name__)
SECRET_KEY = os.urandom(32)
app.config["SECRET_KEY"] = SECRET_KEY


class ContactForm(FlaskForm):
    name = StringField("Name")
    email = StringField("Email")
    subject = StringField("Subject")
    message = TextAreaField("Message")
    submit = SubmitField("Send")


@app.route("/", methods=["POST", "GET"])
def index():
    return render_template("index.html")


@app.route("/resume")
def resume():
    return render_template("resume.html")


@app.route("/projects")
def projects():
    return render_template("projects.html")


@app.route("/contact", methods=["POST", "GET"])
def get_contact():
    form = ContactForm()
    if request.method == "POST":
        name = request.form["name"]
        email = request.form["email"]
        subject = request.form["subject"]
        message = request.form["message"]
        res = pd.DataFrame(
            {"name": name, "email": email, "subject": subject, "message": message},
            index=[0],
        )
        # res.to_csv('./contactUsMessage.csv')

        con = sqlite3.connect(
            "contactsPage.db"
        )  # create/connect to sqlite db and thene ccreate a cursor to execute cmds
        cur = con.cursor()
        cur.execute(
            """CREATE TABLE IF NOT EXISTS contactsPage
            (sku text PRIMARY KEY, name text, email text, subject text, message text)"""
        )
        cur.executemany("INSERT INTO contactsPage VALUES (?, ?, ?, ?)", res)
        cur.close()
        con.commit()
        db.connections.close_all()
        return render_template("ThankYou.html")
    else:
        return render_template("contact.html", form=form)


if __name__ == "__main__":
    app.run(debug=True)
