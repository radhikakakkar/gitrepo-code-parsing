from fastapi import FastAPI, Path, Request, HTTPException, Header, Depends, Form
from passlib.context import CryptContext
import uuid
import firebase_admin
from firebase_admin import auth
from firebase_admin import credentials
import pyrebase
from authentication.verify_token import verify_token
from model import UserSchema, UserLoginSchema
from core.data_saving import (
    get_repo_name,
    insert_repo,
    get_file_names,
    extract_meta_data,
)
from core.data_fetching import (
    deliver_file_names,
    deliver_function_names,
    deliver_function_code,
    deliver_class_names,
)
from db import db, repositories_data, files_data, functions_data, users_data


#firebase 
if not firebase_admin._apps:
    # app/config/momentum-fdc60-firebase-adminsdk-qx0o6-5e1da83d47.json
    
    cred = credentials.Certificate("/Users/radhikakakkar/My Projects/momentum/app/config/momentum-fdc60-firebase-adminsdk-qx0o6-5e1da83d47.json")
    firebase_admin.initialize_app(cred)

firebaseConfig = {
  "apiKey": "AIzaSyCIvDys_3_lf1h9vGUECjXU-YrJwKuzZHQ",
  "authDomain": "momentum-fdc60.firebaseapp.com",
  "projectId": "momentum-fdc60",
  "storageBucket": "momentum-fdc60.appspot.com",
  "messagingSenderId": "465335188572",
  "appId": "1:465335188572:web:ee4b21450e7c3892917a99",
  "measurementId": "G-5TQT184RB1",
  "databaseURL": ""
}
firebase = pyrebase.initialize_app(firebaseConfig)


app = FastAPI()

# routes
@app.post("/user-signup")
def post(user_data: UserSchema):
    user = user_data.__dict__
    
    try:
        existing_user = auth.get_user_by_email(user["email"])
        return {"status": "error", "message": "User already exists"}
    except firebase_admin.auth.UserNotFoundError:
        try:
            # Create the user
            print("Creating the user")
            auth.create_user(
                email=user_data.email,
                password=user_data.password
            )
            return {"status": "success", "message": "User created successfully"}
        except Exception as e:
            print(f"Error while creating user: {e}")
            raise HTTPException(status_code=400, detail=f"Firebase Auth Error while creating new user: {e}")
    except Exception as e:
        print(f"Error while checking existing user: {e}")
        raise HTTPException(status_code=500, detail=f"Firebase Auth Error when checking for already present user: {e}")

@app.post("/user-login")
def post(user_data: UserLoginSchema):
    try:
        user_credentials = firebase.auth().sign_in_with_email_and_password(
            email=user_data.email,
            password=user_data.password
        )
        print(user_credentials)
        token = user_credentials['idToken']
        return {"status": "success", "message": "User logged in successfully", "token": token}
    except Exception as e:
        print(f"Error while logging in: {e}")
        raise HTTPException(status_code=400, detail=f"Firebase Auth Error when logging in: {e}")

@app.get("/")
def get():
    return {"message": "hello you!"}


# routes to save data
@app.post("/submit-github-repo")
def post(repo_link: str = Form(...), verified_user: bool = Depends(verify_token)):
    print("I'm inside")
    if not verified_user:
        return {"status": "error", "message": "User not authenticated!"}
    repo_data = {"url": repo_link}
    result = insert_repo(repo_data)
    return result


@app.post("/extract-meta-data")
def post(repo_name: str = Form(...), verified_user: bool = Depends(verify_token)):  # will take take the variable from the URL param or try to access the request body?
    
    if not verified_user:
        return {"status": "error", "message": "User not authenticated!"}
    check_repo_in_db = repositories_data.find_one({"name": repo_name})
    if check_repo_in_db and check_repo_in_db["data_bool"]:
        return {
            "status": "already done",
            "message": "Data for this repo is already present in DB",
        }
    elif check_repo_in_db:
        save_data_in_db = extract_meta_data(repo_name)
        if save_data_in_db["status"] == "done":
            print(check_repo_in_db)
            print(check_repo_in_db["data_bool"])
            # check_repo_in_db["data_bool"] = True
            repositories_data.update_one(
                {"name": repo_name},
                {"$set": {"data_bool": True}}
            )
            return {
                "status": "done",
                "message": "All neccessary data extracted and temp files deleted!",
            }
        else:
            return {"status": "error", "message": save_data_in_db["message"]}
    else:
        return {"status": "error", "message": "repo has not been submitted"}


# route to fetch function names in the current file
@app.get("/get-file-names/{repo_name}")
def get(repo_name: str, verified_user: bool = Depends(verify_token)):
    if not verified_user:
        return {"status": "error", "message": "User not authenticated!"}
    file_names_result = deliver_file_names(repo_name)

    if file_names_result["status"] == "success":
        file_names_data = file_names_result["data"]
        return {"status": "success", "message": file_names_result["message"]}
    else:
        return {"status": "error", "message": {file_names_result["message"]}}


@app.get("/get-function-names/{file_name}")
def get(file_name: str, verified_user: bool = Depends(verify_token)):
    if not verified_user:
        return {"status": "error", "message": "User not authenticated!"}
    function_names_result = deliver_function_names(file_name)

    if function_names_result["status"] == "success":
        return {"status": "success", "message": function_names_result["message"]}
    else:
        return {"status": "error", "messages": function_names_result["message"]}


@app.get("/get-function-code/{function_name}")
def get(function_name: str, verified_user: bool = Depends(verify_token)):
    if not verified_user:
        return {"status": "error", "message": "User not authenticated!"}
    function_code_result = deliver_function_code(function_name)
    if function_code_result["status"] == "success":
        return {"status": "success", "message": function_code_result["message"]}
    else:
        return {"status": "error", "message": function_code_result["message"]}


@app.get("/get-class-name/{file_name}")
def get(file_name: str, verified_user: bool = Depends(verify_token)):
    if not verified_user:
        return {"status": "error", "message": "User not authenticated!"}
    class_name_result = deliver_class_names(file_name)
    if class_name_result["status"] == "success":
        return {"status": "success", "message": class_name_result["message"]}
    else:
        return {"status": "error", "message": class_name_result["message"]}


