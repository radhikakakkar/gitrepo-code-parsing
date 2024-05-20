from db import db, repositories_data, files_data, functions_data, classes_data


def deliver_file_names(repo_name: str):
    # check if repo name exists in DB
    repo_doc = repositories_data.find_one({"name": repo_name})
    if repo_doc is not None:
        repo_id = repo_doc["_id"]
        # check if data for this repo has been parsed (data_bool)
        if repo_doc["data_bool"]:
            files = files_data.find({"repo_id": repo_id})
            # we can add another condition to check if the repo has any files at all
            file_names = [file["name"] for file in files if "name" in file]
            print(file_names)
            print(type(file_names))
            return {
                "status": "success",
                "message": f"The File names for {repo_name} are {file_names}",
                "data": file_names,
            }
        else:
            return {
                "status": "error",
                "message": f"The data for the {repo_name} has not yet been parsed. (Use the extract_meta_data route first)",
            }
    else:
        return {
            "status": "error",
            "message": f"The {repo_name} has not been submitted to the DB. (Use submit-github-repo route first)",
        }


def deliver_function_names(file_name: str):
    # check is this file is present in DB
    file_doc = files_data.find_one({"name": file_name})
    if file_doc is not None:
        file_id = file_doc["_id"]
        print(file_id)
        # check if functions_data has any docs with this file id
        functions = functions_data.find({"file_id": file_id})
        function_names = [
            function_single["name"]
            for function_single in functions
            if "name" in function_single
        ]
        print(type(function_names))
        print(function_names)
        # check if the retrieved data has some documents in it
        # if len(function_names) > 0:
        if function_names:
            return {
                "status": "success",
                "message": f"The function names for file: {file_name} are {function_names}",
                "data": function_names,
            }
        else:
            return {
                "status": "error",
                "message": f"There are no functions in the file: {file_name}. Try looking for class names",
            }
    else:
        return {
            "status": "error",
            "message": f"There is no file with name {file_name}. Please Retry!",
        }


def deliver_function_code(function_name: str):
    # check if function is present in DB
    function_data = functions_data.find_one({"name": function_name})
    if function_data is not None:
        function_code = function_data["code"]
        return {
            "status": "success",
            "message": f"The Code for function: {function_name} is -- {function_code}",
            "data": function_code,
        }
    else:
        return {
            "status": "error",
            "message": f"There is no function with name {function_name}. Please Retry!",
        }


def deliver_class_names(file_name: str):
    # check is this file is present in DB
    file_doc = files_data.find_one({"name": file_name})
    if file_doc is not None:
        file_id = file_doc["_id"]
        print(file_id)
        # check if functions_data has any docs with this file id
        classes = classes_data.find({"file_id": file_id})
        class_names = [
            class_single["name"] for class_single in classes if "name" in class_single
        ]
        print(type(class_names))
        print(isinstance(class_names, list))
        print(class_names)
        # check if the retrieved data has some documents in it
        # if len(class_names) > 0:
        if class_names:
            return {
                "status": "success",
                "message": f"The class names for file: {file_name} are {class_names}",
                "data": class_names,
            }
        else:
            return {
                "status": "error",
                "message": f"There are no classes in the file: {file_name}. Try looking for function names",
            }
    else:
        return {
            "status": "error",
            "message": f"There is no file with name {file_name}. Please Retry!",
        }
