#Stephen Huang's  web application project code for 12 Software Engineering and Computer Science.
import os
#Importing everything we need.
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

#app.route is used for mapping urls.
@app.route('/', methods=["GET", "POST"])
@app.route('/home', methods=["GET", "POST"])

#Python code for the home page.
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
    champions = Champion.query.all() #Queries all the champions so they can be displayed in a table in home.html. 
    return render_template("home.html", champions=champions)
#Python code for the editor page.
@app.route('/edit', methods=["GET", "POST"])
def edit(): 
    champions = None
    champions = Champion.query.all()
    return render_template("edit.html", champions=champions)
#Python coe for the feedback page.
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
#This function def update() allows users to change any champions name.
@app.route("/update", methods=["POST"])
def update():
    try:
        newname = request.form.get("newname") #First we request the new name.
        oldname = request.form.get("oldname") #Then we look for the old name.
        champion = Champion.query.filter_by(name=oldname).first() #Finds the first champion that matches the old name.
        champion.name = newname #Replace that champions old name with the new one.
        db.session.commit() #Commit to the DB.
    except Exception as e:
        print("Couldn't update champion name")
        print(e)
    return redirect("/")
#This function def updaterole() allows users to change any champion's role. 
@app.route("/updaterole", methods=["POST"])
def updaterole():
    try:
        newrole = request.form.get("newrole") #First we request the new role.
        oldrole = request.form.get("oldrole") #Then we look for the old role.
        champion = db.session.query(Champion).\
            filter_by(name=oldrole).first()   #Finds the champion we're trying to change using their name                           
        champion.role = newrole #Replace their current role with the new one.
        db.session.commit() #Commmit to the DB.
    except Exception as e:
        print("Couldn't update role")
        print(e)
    return redirect("/")
#This function def updateregion() allows users to change any champion's region.
@app.route("/updateregion", methods=["POST"])
def updateregion():
    try:
        newregion = request.form.get("newregion") #First we request for their new region.
        oldregion = request.form.get("oldregion") #Then we take their old region.
        champion = Champion.query.filter_by(name=oldregion).first() #Find the name of the champion that we're changing the region of.
        champion.region = newregion #Replace their current region with the newly chosen one.
        db.session.commit() #Commit tthis change to the DB.
    except Exception as e:
        print("Couldn't update region")
        print(e)
    return redirect("/")
#This function def updatechamp_class() allows uers to change any champions classification.
@app.route("/updatechamp_class", methods=["POST"])
def updatechamp_class():
    try:
        newchamp_class = request.form.get("newchamp_class") #First we request for their new class.
        oldchamp_class = request.form.get("oldchamp_class") #Then we take their old class.
        champion = Champion.query.filter_by(name=oldchamp_class).first() #Find the name of the champion whose class is being updated.
        champion.champ_class = newchamp_class #Updates their old class to the new one.
        db.session.commit() #Commit this change to the DB.
    except Exception as e:
        print("Couldn't update class")
        print(e)
    return redirect("/")
#This function def delete() allows users to delete a champion from the database.
@app.route("/delete", methods=["POST"])
def delete():
    name = request.form.get("name") #First we request the name of the champion that's to be deleted.
    champion = Champion.query.filter_by(name=name).first() #Query the database using that name.
    db.session.delete(champion) #Delete the champion with that name. 
    db.session.commit() #Commit this to the DB.
    return redirect("/") 
#This function def deletepost() allows for posts to be deleted.
@app.route("/deletepost", methods=["POST"])
def deletepost():
    title = request.form.get("title") #First we request the title of the post that's to be deleted.
    post = Post.query.filter_by(title=title).first() #Query the post database using that title.
    db.session.delete(post) #Delete the post with that title.
    db.session.commit() #Commit to the DB.
    return redirect("/forums")

if __name__ == "__main__":
    app.run(debug=True) #Runs the app.
