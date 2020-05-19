import os

from flask import Flask 
from flask  import render_template
from flask import request
from flask import redirect
from flask_sqlalchemy import SQLAlchemy


project_dir = os.path.dirname(os.path.abspath(__file__))
database_file = "sqlite:///{}".format(os.path.join(project_dir, "leaguedatabase.db"))

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = database_file

db = SQLAlchemy(app)

class Champion(db.Model):
    name = db.Column(db.String(80), unique=True, nullable=False, primary_key=True)
    role = db.Column(db.String(80), unique=False, nullable=False, primary_key=False) 
    region = db.Column(db.String(80), unique=False, nullable=False, primary_key=False)

    def __repr__(self):
        return "<name: {}>".format(self.name)

@app.route('/', methods=["GET", "POST"])
def home(): 
    champions = None
    if request.form:
        try:
            champion = Champion(name=request.form.get("name"), role=request.form.get("role"), region=request.form.get("region"))
            db.session.add(champion)
            db.session.commit()
        except Exception as e:
            print("Failed to add champion")
            print(e)
    champions = Champion.query.all()
    return render_template("home.html", champions=champions)

@app.route("/update", methods=["POST"])
def update():
    try:
        newtitle = request.form.get("newtitle")
        oldtitle = request.form.get("oldtitle")
        champion = Champion.query.filter_by(name=oldtitle).first()
        champion.name = newtitle
        db.session.commit()
    except Exception as e:
        print("Couldn't update champion name")
        print(e)
    return redirect("/")

@app.route("/updateauthor", methods=["POST"])
def updateauthor():
    try:
        newauthor = request.form.get("newauthor")
        oldauthor = request.form.get("oldauthor")
        champion = Champion.query.filter_by(role=oldauthor).first()
        champion.role = newauthor
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
        champion = Champion.query.filter_by(region=oldregion).first()
        champion.region = newregion
        db.session.commit()
    except Exception as e:
        print("Couldn't update region")
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
