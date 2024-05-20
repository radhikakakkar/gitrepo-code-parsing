import os
from git import Repo, GitCommandError
import shutil
import re
from db import db, repositories_data, files_data, functions_data, classes_data
from .tree_sitter_parsing import (
    parse_files_for_function_data,
    parse_files_for_class_data,
)


def get_repo_name(url):
    match = re.search(r"github\.com/[^/]+/([^/]+)", url)
    if match:
        return match.group(1)
    return None


def insert_repo(repo_data):
    # get the repo_name from repo link and save it in the db as well
    repo_name = get_repo_name(repo_data["url"])
    repo_data["name"] = repo_name
    repo_data["data_bool"] = False
    print(repo_data)
    result = repositories_data.insert_one(repo_data)

    if result.acknowledged:
        return {"status": "done", "msg": "repository link saved in DB"}
    else:
        return {"status": "error", "msg": "repository link saving error"}


# extract and save file names
def get_file_names(repo_dir, repo_name, repo_object_id):
    file_names = []
    for root, _, files in os.walk(repo_dir):
        for file in files:
            # print(file)
            file_path = os.path.join(root, file)
            file_names.append({"file_name": file, "file_path": file_path})
    print(len(file_names))
    # save file_names in files_data
    relevant_file_paths = []

    for elem in file_names:
        if elem["file_name"].endswith(".py"):
            relevant_file_paths.append(elem["file_path"])
            update_files_data = files_data.insert_one(
                {
                    "name": elem["file_name"],
                    "path": elem["file_path"],
                    "repo_id": repo_object_id,
                }
            )
            if not update_files_data.acknowledged:
                return {"status": "error", "message": "error saving file names"}
    return {
        "status": "done",
        "message": "file names saved in files_data collection",
        "data": relevant_file_paths,
    }


# extract function names for each file and save function names as seperate docs in functions_data along with the file_id
def get_function_names(file_paths):
    for file_path in file_paths:
        print(file_path)
        file_function_data = parse_files_for_function_data(
            file_path
        )  # giving all the functions names and data in a list of objects
        # print(f" data for {file_path} {file_function_data}")
        # print(f" type for data for {file_path} {type(file_function_data)}")
        if len(file_function_data) != 0:
            # append file's object ID to all docs before inserting into DB
            current_file_doc = files_data.find_one({"path": file_path})
            current_file_id = current_file_doc["_id"]
            print(f" data for {file_path} {file_function_data}")
            # print(type(file_function_data))

            for function_data in file_function_data:
                function_data["file_id"] = current_file_id

            update_funtions_data = functions_data.insert_many(file_function_data)
            if not update_funtions_data.acknowledged:
                return {
                    "status": "error",
                    "message": "error saving function data for {file_path}",
                }
        # else:
        #     return {"status": "error", "message": "The current file does not have any functions! sorr"}

    return {"status": "done", "message": "function data saved for all relevant files"}


# extract file for class data and save class_names as seperate docs in classes_data along with file_id
def get_class_names(file_paths):
    for file_path in file_paths:
        file_class_data = parse_files_for_class_data(file_path)
        print(f" data for {file_path} {file_class_data}")
        print(
            f" type for data for {file_path} {type(file_class_data)}"
        )  # should be list
        if len(file_class_data) != 0:
            # append file's object ID to all docs before inserting into DB
            current_file_doc = files_data.find_one({"path": file_path})
            current_file_id = current_file_doc["_id"]
            print(f" data for {file_path} {file_class_data}")
            # print(type(file_class_data))

            for class_data in file_class_data:
                class_data["file_id"] = current_file_id

            update_class_data = classes_data.insert_many(file_class_data)
            if not update_class_data:
                return {
                    "status": "error",
                    "message": "error saving class data for {file_path}",
                }

    return {"status": "done", "message": "class data saved for all relevant files"}


# extract all meta data
def extract_meta_data(repo_name):
    repo_doc = repositories_data.find_one({"name": repo_name})
    repo_url = repo_doc["url"]
    repo_object_id = repo_doc["_id"]
    repo_dir = f"./git_code/{repo_name}"
    try:
        Repo.clone_from(repo_url, repo_dir)
    except GitCommandError as e:
        return {"status": "error", "message": f"Failed to clone repository: {str(e)}"}

    # get file names
    file_names = []
    file_names_result = get_file_names(repo_dir, repo_name, repo_object_id)
    if file_names_result["status"] == "done":
        file_names = file_names_result["data"]

    # get function names
    functions_data_result = get_function_names(file_names)

    # get class names
    class_data_result = get_class_names(file_names)

    # deleting repository
    shutil.rmtree(repo_dir)

    if (
        file_names_result["status"] == "done"
        and functions_data_result["status"] == "done"
        and class_data_result["status"] == "done"
    ):
        # data parsed bool in repositories doc should be True
        # repo_object_id["data_bool"] = True
        # done the above in routes
        return {"status": "done", "message": "Data saved in DB"}
    else:
        return {"status": "error", "message": "error saving data"}
