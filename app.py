from flask import Flask, render_template, request, url_for, flash, redirect
import sqlite3
app = Flask(__name__)

connection = sqlite3.connect("users_data.db")
cursor = connection.cursor()
command = """CREATE TABLE IF NOT EXISTS users(name TEXT, password TEXT)"""
cursor.execute(command)
@app.route("/")
def hello_world():
    return render_template("index.html", title="Hello")

@app.route("/register", methods=['GET', 'POST'])
def register():
    if (request.method == 'POST'):
        print(request.form['fullname'])
    # jaatrod kodu, ka sanemt datus no html formas uz python puses (python kodaa)

    return render_template("register.html", title="Registration")