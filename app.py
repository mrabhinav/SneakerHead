from logging import debug
import sqlite3
from os import name
from types import MethodDescriptorType
from flask import Flask, render_template, request, session
from werkzeug.utils import redirect
app = Flask(__name__)
import datetime
app.config["SECRET_KEY"] = "1234"
@app.route('/home')
@app.route('/')
def index():
    return render_template("index.html")

@app.route('/login', methods = ["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")
    message = ""
    username = request.form.get ("username")
    password = request.form.get ("password")
    firstname = session.get("firstname_reg")
    lastname = session.get("lastname_reg")
    location = session.get("location_reg")
    email = session.get("email_reg")
    print(email)
    username_reg = session.get("username_reg", "Username not found")
    password_reg = session.get("password_reg", "Password not found")
    if username == username_reg:
        if password == password_reg:
            message = "Login Successful"
            conn = sqlite3.connect ('userdata.db')
            cur = conn.cursor()
            cur.execute("INSERT INTO userdata (firstname, lastname, username,location, email, password) VALUES(?,?,?,?,?,?);", (firstname,lastname, username,location, email,password))
            print("Values Inserted")
            session["athenticated"] = True
            conn.commit()
            conn.close()
            return render_template ("quiz.html", message = message, email = email, username = username) 

        else:
            message = "Password does not match"
            return render_template ("login.html", message = message)
    else:
        message = "User is not found"
        return render_template ("login.html", message = message)

@app.route("/users")
def users():
    conn = sqlite3.connect ('userdata.db')
    cur = conn.cursor()
    records = cur.execute("SELECT * FROM userdata") .fetchall()
    return render_template ("users.html", records = records)

@app.route("/logout")
def logout():
    session["athenticated"] = False
    return render_template ("login.html", message = "You have been successfully logged out")

@app.route('/signup', methods = ["GET", "POST"])
def signup():
    if request.method == "GET":
        return render_template("signup.html")
    firstname = request.form.get ("firstname")
    lastname = request.form.get ("lastname")
    username = request.form.get ("username")
    email = request.form.get ("email")
    location = request.form.get ("place")
    password = request.form.get ("password")
    confirmpassword = request.form.get ("cpassword")
    if password == confirmpassword :
        session["password_reg"] = password
        session["username_reg"] = username
        session["email_reg"] = email
        session["firstname_reg"] = firstname
        session["lastname_reg"] = lastname
        session["location_reg"] = location
        conn = sqlite3.connect ('userdata.db')
        cur = conn.cursor()
        records = cur.execute ("SELECT * FROM userdata") .fetchall()
        if records != []:
            email_data = []
            for record in records:
                email_data.append(record[5])
                print(email_data)
                if email in email_data:
                    return render_template("signup.html", message = "Email Already Exists")
    
        return render_template('login.html', message = "registered sucessfully")
    else:
        return render_template("signup.html", message = "passwords do not match")
    
@app.route('/profile')
def profile():
    username_reg = session.get("username_reg", "Username not found")
    password_reg = session.get("password_reg", "Password not found")
    email_reg = session.get("email_reg", "Email not found")
    firstname_reg = session.get("firstname_reg", "First Name not found")
    lastname_reg = session.get("lastname_reg", "Last Name not found")
    fullname = firstname_reg + " " + lastname_reg
    location = session.get("location_reg", "Location not Found")
    return render_template ("profile.html", username = username_reg, email = email_reg, name = fullname, location = location)


@app.route("/validatepassword", methods = ["POST"])
def validatepassword():
    password = request.form.get ("inputverfication")
    spacecount = 0
    length = len(password)
    lowcharcount = 0
    uppercharcount = 0
    digitcount = 0
    speccount = 0
    for i in password:
        if i.islower():
            lowcharcount+=1
        elif i.isupper():
            uppercharcount+=1
        elif i.isdigit():
            digitcount+=1
        elif i.isspace():
            spacecount+=1
        else:
            speccount+=1    
    password_list = [lowcharcount, spacecount, length, uppercharcount, digitcount, speccount]
    return render_template ("verification.html", results = password_list)
    
@app.route ("/verification")
def verification():
    return render_template("verification.html")
@app.route('/alphabet')
def alphabet():
    return render_template("alphabet.html")

@app.route("/result")
def result():
    character = request.args.get ("alphabet")
    ord_value = 0
    difference = 0
    chr_value = ""
    if character >= "a" and character <= "z":
        ord_value = ord(character)
        difference = ord_value - 32
        chr_value = chr(difference)
        return render_template("alphabet.html", result = chr_value)
    else:
        return render_template("alphabet.html", result = "Invalid Character")

@app.route('/calculator')
def calc ():
    return render_template ("calculator.html")

@app.route('/calculated', methods=["POST"])
def calculated ():
    num1 = request.form.get ("firstnum")
    num2 = request.form.get ("secondnum")
    user_input = request.form.get ("calc")
    num1 = float(num1)
    num2 = float(num2)
    result = 0
    if user_input == "addition":
        result = num1 + num2
    elif user_input == "subtraction":
        result = num1 - num2
    elif user_input == "multiplication":
        result = num1 * num2
    elif user_input == "division":
        result = num1 / num2
    else:
        return render_template ("calculator.html", message = "Error")
    return render_template ("calculator.html", result = result)

@app.route('/quiz')
def quiz():
    return render_template("quiz.html")

@app.route('/correctanswer', methods=["POST"])
def correctanswer ():
    user_choice = request.form.get ("answer")
    score = 0
    message = ""
    if user_choice == "answer3":
        score = score+10
        message = "Great Job, Right Answer!"
    else:
        score = score-5
        message = "Wrong Answer"
    return render_template("quiz.html", score = score, message = message)

@app.route ('/cart')
def cart ():
    return render_template("shoppingcartpage.html")

# Certifcation
@app.route ('/form')
def form():
    return render_template("form.html")

@app.route ('/certificate', methods=["POST"])
def certificate():
    firstname= request.form.get('firstname')
    lastname = request.form.get('lastname')
    fullname = firstname + " " + lastname
    course = request.form.get('course')
    grade = 0
    grade = request.form.get('grade')
    gradeper = grade + "%"
    timepy = datetime.date.today()
    return render_template("certificate.html", name = fullname, course = course, grade = gradeper, time = timepy)

    

if __name__ == "__main__":
    app.run(debug=True)



