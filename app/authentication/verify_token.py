from fastapi import HTTPException, Header, Request
import firebase_admin
from firebase_admin import auth
from firebase_admin import credentials
from firebase_admin import app_check

from db import users_data
import jwt

def verify_token(request: Request, Authorization: str = Header(...)):
    if not Authorization:
        raise HTTPException(status_code=401, detail="Authorization header is missing")
    try:
        token = Authorization.split(" ")[1]
        app_check_claims = app_check.verify_token(token)
        
    except Exception as e:
        raise HTTPException(status_code=401, detail=f"Token verification failed: {str(e)}") 
   
    
    




 # decoded_token = firebase_admin.auth.verify_custom_token(token)
 # decoded_token = jwt.decode(token, secret,"HS256")