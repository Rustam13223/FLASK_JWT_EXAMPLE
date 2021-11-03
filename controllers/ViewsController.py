from flask import render_template, jsonify, request, redirect, flash, url_for, make_response
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import set_access_cookies, unset_jwt_cookies
from flask_jwt_extended import jwt_required
from flask_jwt_extended import create_access_token
from app import mongo, jwt
from bson import ObjectId

@jwt.invalid_token_loader
def invalid_token(e):
    res = make_response(redirect(url_for(".sign_in")))
    unset_jwt_cookies(res)
    return res


def redir():
    return redirect('/sign_in')

@jwt_required(optional=True)
def sign_up():
    current_user = get_jwt_identity()
    if current_user:
        return redirect(url_for(".home"))

    if request.method == "POST":
        if not request.form["username"]:
            flash("Please input username!", "error")
        elif not request.form["password"]:
            flash("Please input password!", "error")
        elif not request.form["password2"]:
            flash("Please confirm password!", "error")
        elif len(request.form["password"]) < 8:
            flash("Password must be more than 7 characters!", "error")
        elif request.form["password"] != request.form["password2"]:
            flash("Passwords must match!", "error")
        else:
            user = mongo.db.users.find_one({"username": request.form["username"]})
            if user:
                flash("Username already exists", "error")
            else:
                hash = generate_password_hash(request.form["password"], method="sha256")
                mongo.db.users.insert({"username": request.form["username"], "password": hash})
                flash("Account created!", "success")
                return redirect("/sign_in")
    return render_template("sign_up.html")


@jwt_required(optional=True)
def sign_in():
    current_user = get_jwt_identity()
    if current_user:
        return redirect(url_for(".home"))

    if request.method == "POST":
        if not request.form["username"]:
            flash("Please input username!", "error")
        elif not request.form["password"]:
            flash("Please input password!", "error")
        else:
            user = mongo.db.users.find_one({"username": request.form["username"]})
            if not user:
                flash("Incorrect username or password", "error")
            else:
                if check_password_hash(user["password"], request.form["password"]):
                    access_token = create_access_token(identity=user["username"])
                    flash("Login success!", "success")
                    res = make_response(redirect(url_for(".home")))
                    set_access_cookies(res, access_token)
                    return res
                else:
                    flash("Incorrect username or password", "error")
    return render_template("sign_in.html")

@jwt_required()
def home():
    current_user = get_jwt_identity()
    return render_template("home.html", current_user=current_user)

def logout():
    res = make_response(redirect(url_for(".sign_in")))
    unset_jwt_cookies(res)
    return res


@jwt_required()
def tasks():
    current_user = get_jwt_identity()
    tasks = mongo.db.tasks.find({"username": current_user})
    return render_template("tasks.html", current_user=current_user, tasks=tasks)

@jwt_required()
def tasks_add():
    current_user = get_jwt_identity()
    data = request.get_json()
    if data["task"] != "":
        mongo.db.tasks.insert({"username": current_user, "text": data["task"]})
    return redirect(url_for(".tasks"))

@jwt_required()
def tasks_delete():
    current_user = get_jwt_identity()
    data = request.get_json()
    print(data["_id"])
    mongo.db.tasks.remove({"_id": ObjectId(data["_id"])})
    return redirect(url_for(".tasks"))
