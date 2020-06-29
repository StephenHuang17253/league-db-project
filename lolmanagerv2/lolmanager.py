#Stephen Huang's project code for 12 Software Engineering and Computer Science.
import os

from flask import Flask 
from flask  import render_template
from flask import request
from flask import redirect
from flask_sqlalchemy import SQLAlchemy

project_dir = os.path.dirname(os.path.abspath(__file__))
database_file = "sqlite:///{}".format(os.path.join(project_dir, "leaguedatabasev2.db")) 
#To figure out where our project path is and set up a database file with its full path and the sqlite:/// prefix to tell SQLAlchemy which database engine we're using.
#Tells our web application where our database will be stored.
app = Flask(__name__, template_folder="templates")
app.config["SQLALCHEMY_DATABASE_URI"] = database_file
#Initialize a connection to the database and keep this in the db variable. We'll use this to interact with my database.
db = SQLAlchemy(app)

class Champion(db.Model):
    name = db.Column(db.String(80), unique=True, nullable=False, primary_key=True)
    role = db.Column(db.String(80), unique=False, nullable=False, primary_key=False, foreign_key=True)
    region = db.Column(db.String(80), unique=False, nullable=False, primary_key=False, foreign_key=True)
    champ_class = db.Column(db.String(80), unique=False, nullable=False, primary_key=False, foreign_key=True)

    def __repr__(self):
        return "<name: {}>".format(self.name)
class Post(db.Model):
    title = db.Column(db.String(80), unique=True, nullable=False, primary_key=True)
    content = db.Column(db.String(80), unique=False, nullable=False)
    rating = db.Column(db.String(80), unique=False, nullable=False)
    op = db.Column(db.String(80), unique=False, nullable=False)

    def __repr__(self):
        return "<name: {}>".format(self.title)


@app.route('/', methods=["GET", "POST"])
@app.route('/home', methods=["GET", "POST"])

def home(): 
    champions = None
    if request.form:
        try:
            champion = Champion(name=request.form.get("name"), role=request.form.get("role"), region=request.form.get("region"), champ_class=request.form.get("champ_class"))
            db.session.add(champion)
            db.session.commit()
        except Exception as e:
            print("Failed to add champion")
            print(e)
    champions = Champion.query.all()
    return render_template("home.html", champions=champions)

@app.route('/edit', methods=["GET", "POST"])
def edit(): 
    champions = None
    champions = Champion.query.all()
    return render_template("edit.html", champions=champions)

@app.route('/forums', methods=["GET", "POST"])
def post(): 
    posts = None
    if request.form:  
        try:
            post = Post(title=request.form.get("title"), content=request.form.get("content"), rating=request.form.get("rating"), op=request.form.get("op"))
            db.session.add(post)
            db.session.commit()
        except Exception as e:
            print("Failed to add post")
            print(e)
    posts = Post.query.all()
    return render_template("forums.html", posts=posts)

@app.route("/update", methods=["POST"])
def update():
    try:
        newname = request.form.get("newname")
        oldname = request.form.get("oldname")
        champion = Champion.query.filter_by(name=oldname).first()
        champion.name = newname
        db.session.commit()
    except Exception as e:
        print("Couldn't update champion name")
        print(e)
    return redirect("/")

@app.route("/updaterole", methods=["POST"])
def updaterole():
    try:
        newrole = request.form.get("newrole")
        oldrole = request.form.get("oldrole")
        champion = db.session.query(Champion).\
            filter_by(name=oldrole).first()                               
        champion.role = newrole
        db.session.commit()
    except Exception as e:
        print("Couldn't update role")
        print(e)
    return redirect("/")

@app.route("/updateregion", methods=["POST"])
def updateregion():
    try:
        newregion = request.form.get("newregion")
        oldregion = request.form.get("oldregion")
        champion = Champion.query.filter_by(name=oldregion).first()
        champion.region = newregion
        db.session.commit()
    except Exception as e:
        print("Couldn't update region")
        print(e)
    return redirect("/")

@app.route("/updatechamp_class", methods=["POST"])
def updatechamp_class():
    try:
        newchamp_class = request.form.get("newchamp_class")
        oldchamp_class = request.form.get("oldchamp_class")
        champion = Champion.query.filter_by(name=oldchamp_class).first()
        champion.champ_class = newchamp_class
        db.session.commit()
    except Exception as e:
        print("Couldn't update class")
        print(e)
    return redirect("/")

@app.route("/delete", methods=["POST"])
def delete():
    name = request.form.get("name")
    champion = Champion.query.filter_by(name=name).first()
    db.session.delete(champion)
    db.session.commit()
    return redirect("/")

@app.route("/deletepost", methods=["POST"])
def deletepost():
    title = request.form.get("title")
    post = Post.query.filter_by(title=title).first()
    db.session.delete(post)
    db.session.commit()
    return redirect("/forums")

if __name__ == "__main__":
    app.run(debug=True)
