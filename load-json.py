import json
from pymongo import MongoClient 
  
  
# Making Connection
myclient = MongoClient("mongodb://localhost:27017/") 

db_names_and_files = [("name_basics", "name.basics.json"), ("title_basics", "title.basics.json"), ("title_principals", "title.principals.json"), ("title_ratings", "title.ratings.json")]  
# database 
db = myclient["291db"]
   
for tuple in db_names_and_files:

    #collection.drop(tuple(0)) # drop if exists
    collection = db[tuple[0]]

    with open(tuple[1]) as file:
        file_data = json.load(file)

    collection.insert_many(file_data)  
