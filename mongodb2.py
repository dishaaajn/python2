import datetime
import hashlib
class users:
    def __init__ (self , name="" ,email="" , password="" , age=0 , gender=""):

        self.name = name
        self.email = email
        self.password = password
        self.age = age
        self.gender = gender
        self.created_on = datetime.datetime.now()

    def add_user_detail(self):
        self.name = input("Enter your name :")
        self.email =  input("Enter your email :")
        self.password =  input("Enter your password :").encode('utf-8')
        self.password = hashlib.sha256(self.password).hexdigest()
        self.age = int( input("Enter your age :"))
        self.gender =  input("Enter your gender :")


# user = users()
# user.add_user_detail()
# print(vars(user))