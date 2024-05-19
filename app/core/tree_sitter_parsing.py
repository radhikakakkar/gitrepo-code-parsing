from tree_sitter import Parser, Language
import os


# PY_LANGUAGE = Language('../build/my-languages.so', 'python')
language_so_path = "/Users/radhikakakkar/My Projects/momentum/app/build/my-languages.so"
PY_LANGUAGE = Language(language_so_path, 'python')
parser = Parser()
parser.set_language(PY_LANGUAGE)


def quote(s):
    return 'In '.join([f"> {line}" for line in s.splitlines()])

def text(node):
    return node.text.decode()

#printing query data
def print_captures(captures):
    for capture, tag in captures:
        print(f"@{tag} | {capture.type}] ({capture.start_byte}: {capture.end_byte})")
        print(quote(text(capture)), "\n")
        # return (quote(text(capture)))

#create a list of all function/class names
# def extract_names(captures):
#     function_names = []
#     for capture, _ in captures:
#         function_name = text(capture)
#         function_names.append(function_name)
#     return function_names

def single_file_function_data_maker(name_captures, code_captures):
    single_file_function_data = []
    for name_capture, _ in name_captures:
        function_name = text(name_capture)
        # Find the corresponding code capture for this function name
        for code_capture, _ in code_captures:
            if code_capture.start_byte > name_capture.start_byte:
                function_code = text(code_capture)
                break
        else:
            function_code = ""  # No code found for this function name
        single_file_function_data.append({"name": function_name, "code": function_code})
    return single_file_function_data


def single_file_class_data_maker(class_captures):
    class_names = []
    for class_capture, _ in class_captures:
        class_name = text(class_capture)
        class_names.append({"name": class_name})
    return class_names

def parse_files_for_function_data(file_path: str):
   
    with open(file_path, 'r') as file:
        source_code = file.read()

    tree = parser.parse(source_code.encode('utf-8'))
    root = tree.root_node
    
    function_name_query = PY_LANGUAGE.query("""(function_definition (identifier) @function.name) """)
    function_code_query = PY_LANGUAGE.query("""
        (function_definition
        body: (block) @function.body)
    """)
    name_captures = function_name_query.captures(root)
    code_captures = function_code_query.captures(root)
    
    single_file_function_data = single_file_function_data_maker(name_captures, code_captures)
    # print(single_file_function_data)

    return single_file_function_data

def parse_files_for_class_data(file_path):

    with open(file_path, 'r') as file:
        source_code = file.read()

    tree = parser.parse(source_code.encode('utf-8'))
    root = tree.root_node

    class_name_query = PY_LANGUAGE.query("""
    (class_definition
        name: (identifier) @class.name)
    """)
    class_captures = class_name_query.captures(root)
    single_file_class_data = single_file_class_data_maker(class_captures)
    print(single_file_class_data)   

    return single_file_class_data

# parse_files_for_class_data('../model.py')











#     function_code_query = PY_LANGUAGE.query("""
#     (function_definition
#         body: (block) @function.body)
# """)
#     class_name_query = PY_LANGUAGE.query("""
#     (class_declaration
#         name: (identifier) @class.name)
# """)