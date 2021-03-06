import os
from flask import (
    Flask, flash, render_template,
    redirect, request, session, url_for)
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from werkzeug.security import generate_password_hash, check_password_hash
if os.path.exists("env.py"):
    import env

app = Flask(__name__)


app.config["MONGO_DBNAME"] = os.environ.get("MONGO_DBNAME")
app.config["MONGO_URI"] = os.environ.get("MONGO_URI")
app.secret_key = os.environ.get("SECRET_KEY")

mongo = PyMongo(app)


@app.route("/get_dogs")
def get_dogs():
    dogs = mongo.db.dogs.find()
    return render_template("dogs.html", dogs=dogs)


@app.route("/")
@app.route("/get_main")
def get_main():
    return render_template("main.html")


# Search option for dogs
@app.route("/search", methods=["GET", "POST"])
def search():
    query = request.form.get("query")
    dogs = list(mongo.db.dogs.find({"$text": {"$search": query}}))
    return render_template("dogs.html", dogs=dogs)


# Registering new user
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        # check if username already exists in db
        existing_user = mongo.db.users.find_one(
            {"username": request.form.get("username").lower()})
        # if username is already taken
        if existing_user:
            flash("Username already exists")
            return redirect(url_for("register"))
        # reistering using workzeug password hashing
        register = {
            "username": request.form.get("username").lower(),
            "password": generate_password_hash(request.form.get("password"))
        }
        mongo.db.users.insert_one(register)

        # put the new user into 'session' cookie
        session["user"] = request.form.get("username").lower()
        flash("Registration Successful!")
        return redirect(url_for("profile", username=session["user"]))
    return render_template("register.html")


# Log In
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        # check if username exists in db
        existing_user = mongo.db.users.find_one(
            {"username": request.form.get("username").lower()})

        if existing_user:
            # ensure hashed password matches user input
            if check_password_hash(
                existing_user["password"], request.form.get("password")):
                    session["user"] = request.form.get("username").lower()
                    flash("Welcome, {}".format(
                        request.form.get("username")))
                    return redirect(url_for(
                        "profile", username=session["user"]))
            else:
                # invalid password match
                flash("Incorrect Username and/or Password")
                return redirect(url_for("login"))

        else:
            # username doesn't exist
            flash("Incorrect Username and/or Password")
            return redirect(url_for("login"))

    return render_template("login.html")


# privilege page
@app.route("/profile/<username>", methods=["GET", "POST"])
def profile(username):
    # session username from db
    username = mongo.db.users.find_one(
        {"username": session["user"]})["username"]

    if session["user"]:
        return render_template("privilege.html", username=username)

    return redirect(url_for("login"))


# log out
@app.route("/logout")
def logout():
    # remove user from session cookie
    flash("You have been logged out")
    session.pop("user")
    return redirect(url_for("login"))


# add a new dog post
@app.route("/add_dog", methods=["GET", "POST"])
def add_dog():
    if request.method == "POST":
        found_partner = "on" if request.form.get("found_partner") else "off"
        dog = {
            "cities_name": request.form.get("cities_name"),
            "post_code": request.form.get("post_code"),
            "dogs_name": request.form.get("dogs_name"),
            "dogs_age": request.form.get("dogs_age"),
            "about_dog": request.form.get("about_dog"),
            "contact_info": request.form.get("contact_info"),
            "img_url": request.form.get("img_url"),
            "found_partner": found_partner,
            "created_by": session["user"]
        }
        mongo.db.dogs.insert_one(dog)
        flash("Your Dog Successfully Added")
        return redirect(url_for("get_dogs"))

    cities = mongo.db.cities.find().sort("cities_name", 1)
    return render_template("add_dog.html", cities=cities)


# edit your dog post
@app.route("/edit_dog/<dog_id>", methods=["GET", "POST"])
def edit_dog(dog_id):
    if request.method == "POST":
        found_partner = "on" if request.form.get("found_partner") else "off"
        submit = {
            "cities_name": request.form.get("cities_name"),
            "post_code": request.form.get("post_code"),
            "dogs_name": request.form.get("dogs_name"),
            "dogs_age": request.form.get("dogs_age"),
            "about_dog": request.form.get("about_dog"),
            "contact_info": request.form.get("contact_info"),
            "img_url": request.form.get("img_url"),
            "found_partner": found_partner,
            "created_by": session["user"]
        }
        mongo.db.dogs.update({"_id": ObjectId(dog_id)}, submit)
        flash("Your Dog Post Successfully Edited")
        return redirect(url_for("get_dogs"))

    dog = mongo.db.dogs.find_one({"_id": ObjectId(dog_id)})
    cities = mongo.db.cities.find().sort("cities_name", 1)
    return render_template("edit_dog.html", dog=dog, cities=cities)


# delete dog post
@app.route("/delete_dog/<dog_id>")
def delete_dog(dog_id):
    mongo.db.dogs.remove({"_id": ObjectId(dog_id)})
    flash("Your Dog Add Successfully Deleted")
    return redirect(url_for("get_dogs"))


# manage cities
@app.route("/get_cities")
def get_cities():
    cities = list(mongo.db.cities.find().sort("cities_name", 1))
    return render_template("cities.html", cities=cities)


# adding new citie
@app.route("/add_cities", methods=["GET", "POST"])
def add_cities():
    if request.method == "POST":
        citie = {
            "cities_name": request.form.get("cities_name")
        }
        mongo.db.cities.insert_one(citie)
        flash("New City Added")
        return redirect(url_for("get_cities"))

    return render_template("add_cities.html")


# for editing cities
@app.route("/edit_cities/<citie_id>", methods=["GET", "POST"])
def edit_cities(citie_id):
    if request.method == "POST":
        submit = {
            "cities_name": request.form.get("cities_name")
        }
        mongo.db.cities.update({"_id": ObjectId(citie_id)}, submit)
        flash("City Successfully Updated")
        return redirect(url_for("get_cities"))

    citie = mongo.db.cities.find_one({"_id": ObjectId(citie_id)})
    return render_template("edit_cities.html", citie=citie)


# for deleting city
@app.route("/delete_cities/<citie_id>")
def delete_cities(citie_id):
    mongo.db.cities.remove({"_id": ObjectId(citie_id)})
    flash("City Successfully Deleted")
    return redirect(url_for("get_cities"))


if __name__ == "__main__":
    app.run(host=os.environ.get("IP"),
            port=int(os.environ.get("PORT")),
            debug=False)
