from flask import *
import datetime
from mongodb3 import mongodb_helper
import hashlib


web_app = Flask('Patient Management System')
db_helper = mongodb_helper()
@web_app.route("/")
def index():
    return render_template("index.html")
@web_app.route("/signup")
def signup():
    return render_template("register.html")

@web_app.route("/add-user" , methods = ["POST"])
def add_user_in_db():
    db_helper.collection=db_helper.db["users"]

    user_data={
        "name":request.form["name"],
        "email":request.form["email"],
        "password":hashlib.sha256(request.form["pswd"].encode('utf-8')).hexdigest() ,
        "created_on":datetime.datetime.now()
    }
    # message = "The data is {name} , {email} , {password} , {created_on}".format_map(user_data)
    # return message
    result = db_helper.insert(user_data)
    session['user_id'] = str(result.inserted_id)
    session['name'] = user_data['name']
    session['email'] = user_data['email']
    return render_template("home.html" , email=session['email'])

@web_app.route("/fetch-user" , methods = ["POST"])
def fetch_user():
    db_helper.collection=db_helper.db["users"]

    user_data ={'email' : request.form["email"],
                'password' : hashlib.sha256(request.form["pswd"].encode('utf-8')).hexdigest()}
    
    result = db_helper.fetch(user_data)
    if len(result)>0:
        user_data=result[0]
        session['email'] = user_data["email"]
        session['name'] = user_data["name"]
        return render_template("home.html" , email =session['email'] , name = session['name'])
    else:
        message="No User Found! Please try again :/"
        return message
        
@web_app.route("/add-patient" , methods = ["POST"])
def add_patient():
    db_helper.collection=db_helper.db["patients"]
    patient_data = {
        "name": request.form["name"],
        "email":request.form["email"],
        "age" : int(request.form["age"]),
        "address" : request.form["address"],
        "gender" : request.form["gender"],
        "created_on": datetime.datetime.now(),
        "doctor_name":session['name'],
        "doctor_email":session['email']
    }
    result = db_helper.insert(document=patient_data)
    message = "Patient added Successfully"
    return message

@web_app.route("/fetch-patients")
def fetch_patients():
    db_helper.collection=db_helper.db["patients"]
    patient_data={
        "doctor_email":session["email"]
    }
    result = db_helper.fetch(query = patient_data)
    if len(result)>0:
        print(result)
        return "patients fetched"
    
    else:
        return "No patient Found! Please try again :/"

def main():
    web_app.secret_key ="doctor-app-key"
    web_app.run()

    

if __name__=="__main__":
    main()
