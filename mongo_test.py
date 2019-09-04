from pymongo import  MongoClient
import re

my_client = MongoClient("mongodb://localhost:27017/")
my_database = my_client['papers']
vi_collection = my_database['vi']

pattern = re.compile("5G", re.IGNORECASE)
myquery = {"$or": [{"title": pattern}, {"content": pattern}]}

myquery = {"$or" : [{"title" : {"$regex" : "\w*5G\w*"}}, {"content": {"$regex" : "\w*5G\w*"}}]}
found_doc = vi_collection.find(myquery)

print(found_doc.count())
# print(found_doc[0]['content'].splitlines())
