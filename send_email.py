import smtplib
from email.mime.text import MIMEText
import smtplib

with open("email_credentials.txt","r") as file:
    lines=file.readlines()

def send_email(email,height,weight,bmi,average_bmi,count):
    from_email=lines[0]
    from_password=lines[1]
    to_email=email

    subject="Your BMI score"
    message="Hey there, your height is <strong>%s</strong> cm and your weight is <strong>%s</strong> kg.<br>Your calculated BMI is <strong>%s</strong>. <br>Average BMI of all is <strong>%s</strong> and that is calculated out of <strong>%s</strong> people. <br>Thanks!"  % (height,weight,bmi,average_bmi,count)

    msg=MIMEText(message, "html")
    msg["Subject"]=subject
    msg["To"]=to_email
    msg["From"]=from_email

    gmail=smtplib.SMTP("smtp.gmail.com", 587)
    gmail.ehlo()
    gmail.starttls()
    gmail.login(from_email, from_password)
    gmail.send_message(msg)
