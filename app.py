from flask import Flask, render_template, redirect, url_for
from wtforms import Form, StringField, validators
from flask_mongoengine import MongoEngine
from flask.globals import request

app=Flask(__name__)
app.config["MONGODB_SETTINGS"]={
    "db":"todo_app_data",
    "host":"localhost",
    "port":27017
}

db = MongoEngine()
db.init_app(app)

class User(db.Document):
    firstname=db.StringField()
    lastname=db.StringField()
    adres=db.StringField()

    def to_json(self):
        return{
            "firstname":self.firstname,
            "lastname":self.lastname,
            "adres":self.adres,
        }

class RegisterForm(Form):
    firstname=StringField(u"First Name", validators=[
                          validators.input_required()])
    lastname= StringField(u"Last Name", validators=[validators.optional()])
    adres= StringField(u"Adres", validators=[validators.optional()])
@app.route("/")
def index():
    
    number=10
    sayilar=[1,2,3,4,5,]
    isim="Emre"
    return render_template("index.html",number=number, sayilar=sayilar, isim=isim)

@app.route("/hakkimizda")
def about():
    return render_template("about.html")

@app.route("/article/<string:id>")
def article(id):
    return "Article Id= " + id

@app.route("/register",methods=["GET","POST"])
def register():
    form=RegisterForm(request.form)

    if request.method == "POST":
        firstname = form.firstname.data
        lastname = form.lastname.data
        adres = form.adres.data

        user=User(firstname=firstname, lastname=lastname, adres=adres)
        user.save()
        return redirect(url_for("register"))
    else:
        users=list(User.objects)
        print(users)
        return render_template("register.html", form=form, users=users)

if __name__=="__main__":
    app.run(debug=True) 