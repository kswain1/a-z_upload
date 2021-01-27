import firebase_admin
#from firebase.firebase import FirebaseAuthentication
from firebase_admin import credentials
from firebase_admin import firestore
from firebase_admin import auth


import os
#use application default credentials 
#cred = credentials.Certificate('/Users/kehlinswain/Documents/software_projects/a-z_upload/network/service-account-file.json')
cred = credentials.Certificate(os.path.join('network','service-account-file.json'))

app = firebase_admin.initialize_app(cred)

user = auth.create_user(
    email='user@example.com',
    email_verified=False,
    phone_number='+15555550100',
    password='secretPassword',
    display_name='John Doe',
    disabled=False)

print('Sucessfully updated user: {0}'.format(user.uid))

email = input("please enter your password: \n")
password = getpass("Enter your password: \n")

user = auth.create_user_with_email_and_password(email,password)
print("success: ")