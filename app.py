from flask import Flask, render_template, request, url_for, flash, redirect

app = Flask(__name__)

@app.route("/")
def hello_world():
    return render_template("index.html", title="Hello")

@app.route("/register", methods=['GET', 'POST'])
def register():
    if (request.method == 'POST'):
        print(request.form['fullname'])
    # jaatrod kodu, ka sanemt datus no html formas uz python puses (python kodaa)

    return render_template("register.html", title="Registration")