from flask import Flask, render_template, request, redirect, url_for, session, flash
from datetime import timedelta
from flask_sqlalchemy import SQLAlchemy
from .import app
from service.models import Users

@app.route("/")
def home():
    return render_template("index.html")
    
@app.route("/view")
def view():
    return render_template("view.html", values=Users.all())

@app.route("/login", methods=['POST', 'GET'])
def login():
    if request.method == "POST":
        user = request.form["nm"]
        
        # Set perm session
        session.permanent = True
        
        #Store session data
        session["user"] = user
        
        found_user = Users.find_by_name(user)

        if found_user:
            session["email"] = found_user.email
        else:
            usr = Users(user, "", )
            usr.create()
        
        flash("Login successful")
        return redirect(url_for("user"))
    else:
        if "user" in session:
            flash("Already logged in!")
            return redirect(url_for("user"))
        return render_template("login.html")

@app.route("/user", methods=["POST", "GET"])
def user():
    email = None
    if "user" in session:
        user = session['user']
        if request.method == "POST":
            email = request.form["email"]
            session["email"] = email
            Users.update(user, email)
            flash("Email was saved")
        else:
            if "email" in session:
                email = session["email"]
        #Take session data
        #user = session["user"]
        return render_template("user.html", email=email)
    
    else:
        # flash(session['user'])
        flash("You are not logged in!")
        return redirect(url_for("login"))
        
@app.route("/logout")
def logout():
    if "user" in session:
        #Take session data
        user = session["user"]
        flash(f"You have been logged out, {user}", "info") # message flashing
    session.pop("user", None)
    session.pop("email", None)
    return redirect(url_for("login"))
    

