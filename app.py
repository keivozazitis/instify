from flask import Flask, render_template, request, url_for, redirect, session
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.sqlite3'
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
        
        user = users.query.filter_by(username = username).first()
        
        if user is None:
            print("doesnt exist")
            return redirect(url_for("login"))
        
        if user.password != password:
            print("invalid password")
            return redirect(url_for("login"))

        session['user-username'] = user.username
        session['user-id'] = user._id

        print(session['user-username'])
        print(session['user-id'])

    

    return render_template("index.html", title="Hello")

@app.route("/register", methods=['GET', 'POST'])
def register():
    if (request.method == 'POST'):
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']

        user = users(username, password, email)
        db.session.add(user)
        db.session.commit()
    

    return render_template("register.html", title="Registration")





@app.route('/view')
def view():
    return render_template("view.html", values=users.query.all())



if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)


