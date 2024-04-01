import os
import requests

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash
from datetime import datetime
from helpers import apology, login_required, userapology, zip_lists

app = Flask(__name__)

app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

db = SQL("sqlite:///project.db")

apiKey = 'b72cd0e11f5249c08c77d00ba717a66b'
api_url = 'https://api.spoonacular.com/food/ingredients/search'
basenutrient_url = 'https://api.spoonacular.com/food/ingredients/'


#login, logout, and register routes reused from finance pset
@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute(
            "SELECT * FROM users WHERE username = ?", request.form.get("username")
        )

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(
            rows[0]["hash"], request.form.get("password")
        ):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""
    # Forget any user_id
    session.clear()
    # Redirect user to login form
    return redirect("/")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    if request.method == "POST":

        username = request.form.get("username")
        password = request.form.get("password")
        cpassword = request.form.get("confirmation")
        exists = db.execute("SELECT * FROM users where username = ?", username)

        if not username.strip() or not password.strip() or not cpassword.strip():
            return apology("Must complete all fields.")
        if password != cpassword:
            return apology("Passwords must match.")
        if exists:
            return apology("Username already exists.")
        hash = generate_password_hash(request.form.get("password"))
        print(username, hash)
        db.execute("INSERT INTO users (username, hash) VALUES(?, ?)", username, hash)
        return redirect("/")
    else:
        return render_template("register.html")


@app.route("/")
@login_required
def index():
    today = db.execute("SELECT * FROM today")
    return render_template("index.html", today=today)


@app.route("/search", methods=["GET", "POST"])
@login_required
def search():

    if request.method == "POST":
        food = request.form.get("search")
        params = {
            'query': food,
            'apiKey': apiKey,
        }
        response = requests.get(api_url, params=params)

        # query to get food id
        if response.status_code == 200:

            data = response.json()
            results = data.get('results', [])

            for food in results:
                id = food['id']
                description = food['name']

                exists = db.execute("SELECT * FROM foods where id = ?", id)
                if not exists:
                    db.execute("INSERT INTO foods (id, description) VALUES (?,?)", id, description)

            table = db.execute("SELECT * FROM foods")

            return render_template("results.html", table=table)

    else:
        #clear results table before each new search
        db.execute("DELETE FROM foods")
        return render_template("search.html")


@app.route("/add", methods=["POST"])
def add():
    id = request.form.get('id')
    description = request.form.get('description')
    url = f"{basenutrient_url}{id}/information"
    servings = request.form.get("servings")
    unit = request.form.get("unit")
    amount = servings + ' ' + unit
    params = {
        'apiKey': apiKey,
        'amount': servings,
        'unit': unit
    }
    #query for nutrient data using food id
    nutrientresponse = requests.get(url, params=params)
    infoods = db.execute("SELECT * FROM foods where id = ?", id)
    if not infoods:
        db.execute("INSERT INTO foods (id, description) VALUES (?,?)", id, description)

    # process nutrient values to show in todays table
    if nutrientresponse.status_code == 200:
        data = nutrientresponse.json()
        results = data.get('nutrition')
        nutrients = results['nutrients']

        db.execute("UPDATE foods set servings = ? where id = ?", amount, id)

        for nutrient in nutrients:
            if nutrient['name'] == 'Calories':
                db.execute("UPDATE foods set calories = ? where id = ?", nutrient['amount'], id)
            if nutrient['name'] == 'Fat':
                db.execute("UPDATE foods set fats = ? where id = ?", nutrient['amount'], id)
            if nutrient['name'] == 'Protein':
                db.execute("UPDATE foods set protein = ? where id = ?", nutrient['amount'], id)
            if nutrient['name'] == 'Carbohydrates':
                db.execute("UPDATE foods set carbs = ? where id = ?", nutrient['amount'], id)


        intoday = db.execute("SELECT * FROM today where id = ?", id)
        if not intoday:
            db.execute("INSERT INTO today (servings, id, description, calories, protein, carbs, fats) SELECT servings, id, description, calories, protein, carbs, fats from foods where id = ?", id)
            db.execute("INSERT INTO history (servings, id, description, calories, protein, carbs, fats) SELECT servings, id, description, calories, protein, carbs, fats from foods where id = ?", id)
            db.execute("UPDATE history set user_id = ?", session["user_id"] )
        return redirect('/')
    else:
        return apology('Could Not Be Added')


@app.route("/reset", methods=["POST"])
def reset():
    db.execute('DELETE FROM today')
    return redirect('/')


@app.route("/history")
@login_required
def history():
    history = db.execute("SELECT * FROM history where user_id  = ?", session["user_id"]  )
    return render_template("history.html", history=history)

@app.route("/planrequest", methods=["GET", "POST"])
@login_required
def planrequest():
    url = 'https://api.spoonacular.com/mealplanner/generate'
    if request.method == "POST":
        calories = request.form.get("calories")
        diet = request.form.get("diet")
        params = {
        'apiKey': apiKey,
        'targetCalories': calories,
        'diet': diet,
        'timeFrame':'day'
        }
        #query for recipes
        response = requests.get(url, params=params)
        if response.status_code == 200:
            data = response.json()
            meals = data.get('meals')
            macros = data.get('nutrients')

            return render_template("planresults.html", meals=meals, macros=macros)
        else:
            return apology("Failed to retrieve meal plan")

    else:
        return render_template("planrequest.html")

@app.route("/fun")
def fun():
    return render_template("fun.html")

@app.route("/joke", methods=["POST"])
def joke():
    url = 'https://api.spoonacular.com/food/jokes/random'
    params = {
        'apiKey': apiKey,
        }
    response = requests.get(url, params=params)
    data = response.json()
    joke = data.get('text')
    print(joke)
    return render_template("joke.html", joke=joke)

@app.route("/trivia", methods=["POST"])
def trivia():
    url = 'https://api.spoonacular.com/food/trivia/random'
    params = {
        'apiKey': apiKey,
        }
    response = requests.get(url, params=params)
    data = response.json()
    trivia = data.get('text')
    print(trivia)
    return render_template("trivia.html", trivia=trivia)
