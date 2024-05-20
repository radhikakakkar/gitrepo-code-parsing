#file to delete all data in DB collections
from db import db, repositories_data, files_data, functions_data, classes_data

result = files_data.delete_many({})
print(result)
result2 = functions_data.delete_many({})
print(result2)
result3 = classes_data.delete_many({})
print(result3)
