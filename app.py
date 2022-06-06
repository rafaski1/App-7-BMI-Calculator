"""
This web app will allow you to calculate your BMI (body mass index) based on the data you input (height and weight).
Script will email you your results and compare it with other entries within the existing database.
Frontend in html and css. backend in python with flask. database with sqlalchemy.
"""
from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from send_email import send_email
from sqlalchemy.sql import func

app=Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"]="postgresql://postgres:postgres1234@localhost/bmi_calculator" #database at localhost
# app.config["SQLALCHEMY_DATABASE_URI"]="postgres://ercovdvrchfiga:fbb28f664eace1c2c041a418bdaf0bb311307e0f7abfcc2118619b4a8adef6d1@ec2-52-206-182-219.compute-1.amazonaws.com:5432/d5fjvta1hg58in?sslmode=require" #database at heroku
db=SQLAlchemy(app)

class Data(db.Model):
    __tablename__="data"
    id=db.Column(db.Integer, primary_key=True)
    email_=db.Column(db.String(120), unique=True)
    height_=db.Column(db.Integer)
    weight_=db.Column(db.Integer)
    bmi_=db.Column(db.Float(3,1))

    def __init__(self, email_, height_, weight_, bmi_):
        self.email_=email_
        self.height_=height_
        self.weight_=weight_
        self.bmi_=bmi_

@app.route("/")
def index():
    return  render_template("index.html")

@app.route("/success", methods=["POST"])
def success():
    if request.method == "POST":
        email=request.form["email_name"]
        height=request.form["height_name"]
        weight=request.form["weight_name"]
        bmi=int(weight)/(float(height)/100)**2
        bmi=round(bmi,1)
        if db.session.query(Data).filter(Data.email_==email).count() == 0: #for not existing emails in database
            data=Data(email,height,weight,bmi)
            db.session.add(data)
            db.session.commit()
            average_bmi=db.session.query(func.avg(Data.bmi_)).scalar()
            average_bmi=round(average_bmi,1)
            count=db.session.query(Data.height_).count() #calculates number of entries
            send_email(email, height, weight, bmi, average_bmi, count)
            return render_template("success.html")
    # renders index.html page again if already existing email was given
    return render_template("index.html", text="Seems like we already have some data from this email!")

if __name__=="__main__":
    app.debug=False
    app.run()