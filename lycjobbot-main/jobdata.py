from pymongo import MongoClient

cluster = MongoClient("mongodb+srv://Egonau:egoregoregor@vacancy.ggsch.mongodb.net/lycjobdata?retryWrites"
                      "=true&w=majority")
db = cluster["lycjobdata"]
ContColl = db["Content"]
PCColl = db["PChelp"]
ProgColl = db["Programming"]
LessColl = db["Lessons"]
VolColl = db["Volontering"]
MarkColl = db["Marketing"]
LangColl = db["Languages"]
ServColl = db["Serving"]