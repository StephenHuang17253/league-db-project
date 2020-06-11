import os

from flask import Flask 
from flask  import render_template
from flask import request
from flask import redirect
from flask_sqlalchemy import SQLAlchemy


project_dir = os.path.dirname(os.path.abspath(__file__))
database_file = "sqlite:///{}".format(os.path.join(project_dir, "leaguedatabase.db"))

app = Flask(__name__, template_folder="templates")
app.config["SQLALCHEMY_DATABASE_URI"] = database_file

db = SQLAlchemy(app)

class Champion(db.Model):
    name = db.Column(db.String(80), unique=True, nullable=False, primary_key=True)
    role = db.Column(db.String(80), unique=False, nullable=False, primary_key=False, foreign_key=True)
    region = db.Column(db.String(80), unique=False, nullable=False, primary_key=False, foreign_key=True)
    champ_class = db.Column(db.String(80), unique=False, nullable=False, primary_key=False, foreign_key=True)

    def __repr__(self):
        return "<name: {}>".format(self.name)


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

if __name__ == "__main__":
    app.run(debug=True)
 