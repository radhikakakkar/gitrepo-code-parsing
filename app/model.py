#database 
from pydantic import BaseModel
from typing import Optional
from bson import ObjectId


#metadata schema  
#Include fields for identifiers, file names, function names, class names, and the code for each function.
class Repositories(BaseModel):
    name: str
    url: str
    # last_updated: str

class File(BaseModel):
    name: str
    repo_id: str
    path: str

class FunctionMetadata(BaseModel):
    name: str
    class_name: str
    file_id: str
    code: str
    





#user schema
# class UserSchema(BaseModel):
#     full_name: str
#     email: str
#     password: str



# class UserLoginSchema(BaseModel):
#     email: str
#     password: str