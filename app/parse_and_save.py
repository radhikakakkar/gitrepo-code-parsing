from tree_sitter import Parser, Language

PY_LANGUAGE = Language('build/my-languages.so', 'python')
parser = Parser()
parser.set_language(PY_LANGUAGE)

# Example: Parse source code from a file
with open('try.py', 'r') as file:
    source_code = file.read()

#sample input code 
source_code = b"""" 
def hello(): 
    print("Hello",  "World")
    print("i am good how are u")
    new_data = []
    print(type(new_data))
"""
# Parse the source code

# tree = parser.parse(bytes(source_code, "utf8"))
tree = parser.parse(source_code)
root = tree.root_node
# print(root)
# print(root.text)

def print_captures(captures):
    for capture, tag in captures:
        print(f"@{tag} | {capture.type}] ({capture.start_byte}: {capture.end_byte})")
        print(quote(text(capture)), "\n")

def quote(s):
    return 'In '.join([f"> {line}" for line in s.splitlines()])

def text(node):
    return node.text.decode()


#function to save the final data in data structure to be sent to DB collection
def print_captures2(captures):
    for capture, tag in captures:
        new_data_list = quote(text(capture))
        print(new_data_list)
        print(type(new_data_list))

#all queries 

#identifier names
# identifier_query = PY_LANGUAGE.query("""
#     (identifier) @identifier
# """)
#file names
# filename_query = PY_LANGUAGE.query("""
#     (translation_unit
#         (preproc_include) @filename)
# """)
#class names
# class_name_query = PY_LANGUAGE.query("""
#     (class_declaration
#         name: (identifier) @class.name)
# """)
# this query function names 
function_name_query = PY_LANGUAGE.query("""(function_definition (identifier) @function.name) """)

# this query gives both function code and names 
function_code_query = PY_LANGUAGE.query("""
    (function_definition
        body: (block) @function.body)
""")

captures = function_code_query.captures(root)
print_captures2(captures)




# captures
# print(captures)

























# print(tree.root_node.sexp())
# tree = tree.root_node.sexp()

# ast_string = """
# module 
# function_definition 
# name: identifier 
# parameters: parameters 
# body: block 
# if_statement 
# condition: identifier 
# consequence: block 
# expression_statement 
# call 
# function: identifier 
# arguments: argument_list
# """




# def extract_information(ast_node):
#     info = {
#         'identifiers': set(),
#         'file_name': '<module>',
#         'functions': []
#     }

#     def extract(node):
#         if isinstance(node, ast.FunctionDef):
#             function_info = {
#                 'name': node.name,
#                 'class_name': None,
#                 'code': ast.unparse(node),
#                 'start_lineno': node.lineno,
#                 'end_lineno': node.end_lineno
#             }
#             if node.parent and isinstance(node.parent, ast.ClassDef):
#                 function_info['class_name'] = node.parent.name
#             info['functions'].append(function_info)
#         elif isinstance(node, ast.Name):
#             info['identifiers'].add(node.id)

#         for child_node in ast.iter_child_nodes(node):
#             extract(child_node)

#     extract(ast_node)
#     return info

# ast_node = ast.parse(ast_string)
# information = extract_information(ast_node)

# print("File Name:", information['file_name'])
# print("Identifiers:", information['identifiers'])
# print("Functions:")

# for function in information['functions']:
#     print("  Name:", function['name'])
#     print("  Class Name:", function['class_name'])
#     print("  Start Line:", function['start_lineno'])
#     print("  End Line:", function['end_lineno'])
#     print("  Code:")
#     print(function['code'])
#     print()
