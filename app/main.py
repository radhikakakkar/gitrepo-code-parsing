from fastapi import FastAPI, Path, Request, HTTPException, Header, Depends
from passlib.context import CryptContext
import uuid
from firebase_admin import auth
from core.data_saving import get_repo_name, insert_repo, get_file_names, extract_meta_data
from core.data_fetching import deliver_file_names, deliver_function_names, deliver_function_code, deliver_class_names
from db import db, repositories_data, files_data, functions_data


app = FastAPI()
    
#routes

#routes to save data 
@app.get("/hi")
def get():
    return {"message": "hello you!"}

@app.post("/submit-github-repo")
def post(repo_link: str):
    repo_data = {
        "url": repo_link
    }
    result = insert_repo(repo_data)
    return result

@app.post("/extract_meta_data")
def post(repo_name: str): # will take take the variable from the URL param or try to access the request body?
    check_repo_in_db = repositories_data.find_one({"name": repo_name})
    if check_repo_in_db and check_repo_in_db["data_bool"]:
        return {"status": "already done", "message": "Data for this repo is already present in DB"}
    elif check_repo_in_db:
        save_data_in_db = extract_meta_data(repo_name)
        if save_data_in_db["status"] == "done":
            check_repo_in_db["data_bool"] = True
            return {"status": "done", "message": "All neccessary data extracted and temp files deleted!"}
        else: 
            return {"status": "error", "message": save_data_in_db["message"]}
    else: 
        return {"status": "error", "message": "repo has not been submitted"}


# route to fetch function names in the current file 

@app.get("/get-file-names/{repo_name}")
def get(repo_name: str):
    file_names_result = deliver_file_names(repo_name)

    if file_names_result["status"] == "success":
        file_names_data = file_names_result["data"]
        return {"status":"success", "message": file_names_result["message"]}
    else:
        return {"status": "error", "message": {file_names_result["message"]}}


@app.get("/get-function-names/{file_name}")
def get(file_name: str):
    function_names_result = deliver_function_names(file_name)
    # print(function_names_result)
    # print(function_names_result["data"])
    # print(type(function_names_result["data"]))

    if function_names_result["status"] == "success":
        return {"status": "success", "message": function_names_result["message"]}
    else: 
        return {"status": "error", "messages": function_names_result["message"]}
    
@app.get("/get-function-code/{function_name}")
def get(function_name: str):
    function_code_result = deliver_function_code(function_name)
    if function_code_result["status"] == "success":
        return {"status": "success", "message": function_code_result["message"]} 
    else: 
        return {"status": "error", "message": function_code_result["message"]}

@app.get("/get-class-name/{file_name}")
def get(file_name: str):
    class_name_result = deliver_class_names(file_name)
    if class_name_result["status"] == "success":
        return {"status": "success", "message": class_name_result["message"]} 
    else: 
        return {"status": "error", "message": class_name_result["message"]}







# async def get_user_firebase(token: str = Depends(auth.verify_id_token)):
#     user = await auth.get_user(token)
#     return user

# @app.post("/user-login")
# async def login(token: str = Depends(get_user_firebase)):
#     return {"user_id": token['uid']}

# @app.get("/protected")
# async def protected_endpoint(user: dict = Depends(get_user_firebase)):
#     return {"message": "This is a protected endpoint", "user": user}


















# #password hashing instance 
# bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated ="auto")

# def create_password_hash(password: str):
#     return bcrypt_context.hash(password)

# def insert_user(user, user_id):
#     user_data = {
#         "user_id": user_id,
#         "full_name": user.full_name,
#         "email": user.email,
#         "password": user.password,
#     }

#     result = users_data.insert_one(user_data)
#     if result.acknowledged:
#         return {"Msg": "User Added Successfull"}
#     else:
#         return {"Msg": " inserting error"}
    
# def check_user(user: UserLoginSchema):
#     return_user = users_data.find_one({"user_id": user.user_id})
#     if return_user:
#         return True
#     else:
#         return False
  
# @app.post("/user/sign-up")
# def sign_up(user: UserSchema):
#     #hashing the password 
#     hashed_password = create_password_hash(user.password)
#     print(hashed_password)
#     user.password = hashed_password

#     user_id = str(uuid.uuid1())
#     insert_user(user, user_id)
#     # return signJWT(user.user_id)
#     return user.user_id



# @app.post("/user/log-in")
# def log_in(user: UserLoginSchema):
#     return_user = users_data.find_one(
#         {"email": user.email}, {"password": user.password}
#     )
#     if return_user:
#         # return signJWT(user.email)
#         return user.email
#     else:
#         return {"Error": "Invalid credetials"}
    