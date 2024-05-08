from flask import Flask, render_template, request, url_for, redirect, session, flash
from flask_sqlalchemy import SQLAlchemy
import requests # type: ignore
import json
from random import randint

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users_1.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = "IUFBAINnfnauionfuanUINFI"
API_KEY = "DeC83FkuGywLwbTUX3nazG6bQh9OjVjt1dLAtZ5ech9h31dn1gYgnned"




db = SQLAlchemy(app)


class users(db.Model):
    _id = db.Column("id", db.Integer, primary_key=True)
    username = db.Column(db.String(100))
    password = db.Column(db.String(100))
    email = db.Column(db.String(100))

    def __init__(self, username, password, email):
        self.username = username
        self.password = password
        self.email = email



@app.route("/", methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user = users.query.filter_by(username = username).first()

        if user is None:
            flash("invalid username")
            return redirect(request.referrer)
        elif user.password != password:
            flash('invalid password')
        else:
        
            session['user_username'] = user.username
            session['user_id'] = user._id

            return redirect(url_for("home"))

    

    return render_template("index.html", title="Hello")

@app.route("/register", methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        confirm_password = request.form['confirm']
        email = request.form['email']

        if confirm_password != password:
            flash("password dont match")
            return redirect(url_for("register"))

        user = users(username, password, email)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for("login"))
    

    return render_template("register.html", title="Registration")


@app.route('/logout')
def logout():
    session.pop('user_id', None)
    session.pop('user_username', None)
    return redirect(url_for('login'))





@app.route('/database')
def view():
    return render_template("database.html", values=users.query.all())

def loadPhotos(ammount):
    API_URL = f'https://api.pexels.com/v1/curated?per_page={ammount}'
    headers = {
        'Authorization': API_KEY
        }
    res = requests.get(API_URL, headers=headers)
    if res.status_code != 200:
        print(f'Error: {res.status_code}')
        
    data = res.json()
    return data


sort_by = 'comments'
@app.route("/instify")
def home():

    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    username = session['user_username']

    data = loadPhotos(200)
    post_data = []
    for photo in data['photos']:
        likes = randint(1, 1000)
        comments = randint(1, 100)
        shares = randint(1, 50)
        x = f'{{"url": "{photo["src"]["original"]}", "name": "{photo["photographer"]}", "likes": "{likes}", "comments": "{comments}", "shares": "{shares}"}}'
        parsed = json.loads(x)
        post_data.append(parsed)
    
    global sort_by
    post_data = sorted(post_data, key=lambda x: int(x[sort_by]), reverse=True)


    return render_template("instify.html", username=username, posts=post_data)

@app.route('/sort_by/<type>')
def sortBy(type):
    global sort_by
    sort_by = type
    return redirect(url_for('home'))

@app.route('/deleteProfile', methods=['GET','POST'])
def deleteProfile():
    print(session['user_id'])
    if request.method == 'GET':
        id = session.get('user_id')
        if id is not None:
            user = users.query.filter_by(_id=id).first()
            if user is not None:
                db.session.delete(user)
                db.session.commit()
                session.pop('user_id')
                session.pop('user_username')
                return redirect(url_for('login'))
    return "Error: Profile deletion failed."

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)


