from pymongo import MongoClient

cluster = MongoClient("mongodb+srv://sasha_smirnov:Sasha17032004@cluster0.andb9.mongodb.net/lycjobdata?retryWrites"
                      "=true&w=majority")
db = cluster["lycjobdata"]
collection = db["lycjobcollection"]
