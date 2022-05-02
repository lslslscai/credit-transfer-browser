from audioop import mul
from django.db import models

from util import get_db_handle

# Create your models here.
def getDataFromDB(db, collection, req, type):
    [db_handle, client] = get_db_handle(
        db,"mongodb://localhost:27017/")
    db_collection = db_handle[collection]
    ret = []
    if type == "all":
        for i in db_collection.find(req,{"pwd": 0, "state": 0}):
            ret.append(i)
        return ret
    else:
        return db_collection.find_one(req,{"pwd": 0, "state": 0})

def adjDataToDB(db, collection, query, set, upsert=False):
    [db_handle, client] = get_db_handle(
        db,"mongodb://localhost:27017/")
    db_collection = db_handle[collection]
    ret = db_collection.update_one(query, set, upsert)
    return ret

def insertDataToDB(db, collection, value):
    [db_handle, client] = get_db_handle(
        db,"mongodb://localhost:27017/")
    db_collection = db_handle[collection]
    ret = db_collection.insert_one(value)
    return ret

def findAndReplace(db, collection, filter, replacement):
    [db_handle, client] = get_db_handle(
        db,"mongodb://localhost:27017/")
    db_collection = db_handle[collection]
    ret = db_collection.find_one_and_replace(filter, replacement)
    return ret

def deleteDataFromDB(db, collection, filter):
    [db_handle, client] = get_db_handle(
        db,"mongodb://localhost:27017/")
    db_collection = db_handle[collection]
    ret = db_collection.delete_one(filter)
    return ret
