# database
from pydantic import BaseModel
from typing import Optional
from bson import ObjectId


# metadata schema
# Include fields for identifiers, file names, function names, class names, and the code for each function.
class Repositories(BaseModel):
    name: str
    url: str
    data_bool: bool
    # last_updated: str


class Files(BaseModel):
    name: str
    repo_id: str
    path: str


class FunctionMetadata(BaseModel):
    name: str
    file_id: str
    code: str


class Classes:
    name: str
    file_id: str


class UserSchema(BaseModel):
    full_name: str
    email: str
    

