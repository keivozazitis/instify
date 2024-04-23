from flask import Flask, render_template, request, url_for, redirect, session, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users_1.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = "IUFBAINnfnauionfuanUINFI"




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
        session.pop('user_username', None)
        session.pop("user_id", None)
        
        user = users.query.filter_by(username = username).first()
        
        if user is None or user.password != password:
            print("doesnt exist")
            flash("user doesnt exist")
            return redirect(request.referrer)
        else:
        
            session['user_username'] = user.username
            session['user_id'] = user._id
            print(session['user_username'])
            print(session['user_id'])

            return redirect(url_for("home", username=user.username))

    

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





@app.route('/database')
def view():
    return render_template("database.html", values=users.query.all())


@app.route("/instify")
def home():
    username = request.args.get('username', None)
    return render_template("instify.html", username=username)



if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)


