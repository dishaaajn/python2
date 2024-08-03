from flask import *
import datetime
from mongodb3 import mongodb_helper
import hashlib
from bson.objectid import ObjectId


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
    return render_template("home.html" , email=session['email'] , name = session["name"])

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
        return render_template("error.html" , email = session["email"] , name = session["name"] , message ="No User Found! Please try again :/")

        
@web_app.route("/add-patient" , methods = ["POST"])
def add_patient():
    if len(session["email"]) == 0:
        return redirect("/")
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
    return render_template("success.html" , email = session["email"] , name = session["name"] , message ="patient added sucessfully")

@web_app.route("/fetch-patients")
def fetch_patients():
    if len(session["email"]) == 0:
        return redirect("/")
    db_helper.collection=db_helper.db["patients"]
    patient_data={
        "doctor_email":session["email"]
    }
    result = db_helper.fetch(query = patient_data)
    if len(result)>0:
        return render_template ("patient-card.html" , patients = result , email = session["email"] , name = session["name"])    
    else:
        return render_template("error.html" , email = session["email"] , name = session["name"] , message ="Patient not found!")

@web_app.route("/logout")
def logout():
    session["email"]=""
    session["name"]=""
    session["user_id"]=""
    session["patient_name"]=""
    session["patient_email"] = ""
    return redirect("/")    
    
@web_app.route("/home")
def home():
    
    if session["name"] == "":
        return render_template("index.html")
    else:
        return render_template("home.html" ,  email = session["email"] , name = session["name"])

@web_app.route("/update-patient/<id>")
def update_patient(id):
    if len(session["email"]) == 0:
        return redirect("/")
    print("patient to be updated:" , id)
    query = {"_id" : ObjectId(id)}
    db_helper.collection= db_helper.db["patients"]
    result = db_helper.fetch(query)
    patient_doc = result[0]
    if len(result) == 0:
        # Handle the case where no patient is found
        return render_template("error.html", email=session["email"], name=session["name"], message="Patient not found!")
    else:
        return render_template("update_patient.html" , 
                                email = session["email"] ,
                                name = session["name"],
                                patient = patient_doc
                            )
    
@web_app.route("/update-consultation/<id>")
def update_consultation(id):
    if len(session["email"]) == 0:
        return redirect("/")
    print("consultation to be updated:" , id)
    query = {"_id" : ObjectId(id)}
    db_helper.collection= db_helper.db["consultations"]
    result = db_helper.fetch(query)
    consultation_doc = result[0]
    if len(result) == 0:
        # Handle the case where no patient is found
        return render_template("error.html", email=session["email"], name=session["name"], message="consultations not found!")
    else:
        return render_template("update-consultation.html" , 
                                email = session["email"] ,
                                name = session["name"],
                                consultation = consultation_doc
                            )
    
@web_app.route("/update-patient-in-db/<id>" , methods = ["POST"])
def update_patient_in_db(id):
    if len(session["email"]) == 0:
        return redirect("/")
    updated_data={
    "name":request.form["name"],
    "email":request.form["email"],
    "age":request.form["age"],
    "address":request.form["address"],
    "gender":request.form["gender"]
    }
    query ={"_id" : ObjectId(id)}
    db_helper.collection= db_helper.db["patients"]
    result = db_helper.update(document_to_update=updated_data , query= query )
    return render_template("success.html" , message = "Patient Updated Successfully" ,   email = session["email"] , name = session["name"])

@web_app.route("/update-consultation-in-db/<id>" , methods = ["POST"])
def update_consultation_in_db(id):
    if len(session["email"]) == 0:
        return redirect("/")
    updated_data={
    "complaints":request.form["complaints"],
    "bp":request.form["bp"],
    "temp":request.form["temp"],
    "sugar":request.form["sugar"],
    "medicines":request.form["medicines"],
    "remarks":request.form["remarks"],
    "Next_Follow_Up":request.form["followup"],
    "patient_name" : session["patient_name"],
    "patient_email" : session["patient_email"],
    "doctor_name" : session["name"],
    "doctor_email" : session["email"]
    }
    query ={"_id" : ObjectId(id)}
    db_helper.collection= db_helper.db["consultations"]
    result = db_helper.update(document_to_update=updated_data , query= query )
    return render_template("success.html" , message = "consultation Updated Successfully" ,   email = session["email"] , name = session["name"])

@web_app.route("/delete-patient/<id>")
def delete_patient(id):
    query={"_id" : ObjectId(id)}
    db_helper.collection= db_helper.db["patients"]
    result = db_helper.delete(query)
    return render_template("success.html" , message = "Patient deleted Successfully" ,  email = session["email"] , name = session["name"] )

@web_app.route("/delete-consultation/<id>")
def delete_consultation(id):
    query={"_id" : ObjectId(id)}
    db_helper.collection= db_helper.db["consultations"]
    result = db_helper.delete(query)
    return render_template("success.html" , message = "consultation deleted Successfully" ,  email = session["email"] , name = session["name"] )

@web_app.route("/add-Consultation/<id>")
def add_consultation(id):

    if len(session["email"]) == 0:
        return redirect("/")
    
    db_helper.collection=db_helper.db["patients"]
    query= {"_id" : ObjectId(id)}
    result = db_helper.fetch(query=query)
    patient_doc = result[0]
    session["patient_name"]=patient_doc["name"]
    session["patient_email"] = patient_doc["email"]
    return render_template("add-consultation.html" ,  email = session["email"] , name = session["name"] , patient_name = session["patient_name"]) 

@web_app.route("/add-consultation-in-db" , methods = ["POST"])
def add_consultation_in_db():
    consultation_data={
        "complaints" : request.form["complaints"],
        "bp" : request.form["bp"],
        "temp" : request.form["temp"],
        "sugar" : request.form["sugar"],
        "medicines" : request.form["medicines"],
        "remarks" : request.form["remarks"],
        "Next_Follow_Up" : request.form["followup"],
        "patient_name" : session["patient_name"],
        "patient_email" : session["patient_email"],
        "doctor_name" : session["name"],
        "doctor_email" : session["email"]
    }
    db_helper.collection=db_helper.db["consultations"]
    result = db_helper.insert(consultation_data)
    return render_template("success.html" , message = "Consultation Added")

@web_app.route("/view-all-consultations")
def view_all_consultation():
    if len(session["email"]) == 0:
        return redirect("/")
    db_helper.collection=db_helper.db["consultations"]
    query={"doctor_email":session["email"]}
    result = db_helper.fetch(query = query)
    print (result)
    if len(result)>0:
        return render_template ("consultations.html" , consultations = result , email = session["email"] , name = session["name"])    
    else:
        return render_template("error.html" , email = session["email"] , name = session["name"] , message ="consultations not found!")
    
@web_app.route("/view-Consultations/<name>")
def view_consultation(name):
    if len(session["email"]) == 0:
        return redirect("/")
    query = {"patient_name" : name,
             "doctor_email":session["email"]}
    db_helper.collection=db_helper.db["consultations"]
    result = db_helper.fetch(query=query)
    print(result)
    if len(result)>0:
        return render_template ("consultations.html" , consultations = result , email = session["email"] , name = session["name"])    
    else:
        return render_template("error.html" , email = session["email"] , name = session["name"] , message ="consultations not found!")
    
@web_app.route("/search_patient")
def search_patient():
    return render_template("search-patient.html" , email = session["email"] , name = session["name"])


@web_app.route("/search-patient-in-db" , methods = ["POST"])
def search_patient_in_db():
    query = {"doctor_email" : session["email"],
             "name" : request.form["name"],
             "email" :  request.form["email"]}
    db_helper.collection=db_helper.db["patients"]
    result = db_helper.fetch(query= query)
    if len(result) == 0:
        return render_template("error.html", email = session["email"] , name = session["name"] , message ="patient not found!") 
    else:
        return render_template("patient-card.html" , patients = result , email = session["email"] , name = session["name"] )

def main():
    web_app.secret_key ="doctor-app-key"
    web_app.run()


if __name__=="__main__":
    main()
