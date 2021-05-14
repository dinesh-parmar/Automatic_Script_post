import motor.motor_asyncio
import urllib
from bson.objectid import ObjectId
from datetime import datetime
import os
import time
import asyncio

MONGO_DETAILS = "mongodb+srv://<USERNAME>:"+urllib.parse.quote("<USERPASSWORD>")+"<HOST_ADDRESS>/<DATABASE_NAME>?retryWrites=true&w=majority"

client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_DETAILS)



def set_the_timezone():
    os.environ['TZ'] = 'Asia/Kolkata' # set new timezone
    time.tzset()

database = client["2ddate"]
def twod_helper(date) -> dict:
    return {
        "id":str(date["_id"]),
        "time": date["time"],
        "twod_value": date["twod_value"],
        "fourd_value":date["fourd_value"]
        }

async def add_time(date:str,time_data: dict) -> dict:
    date_collection = database.get_collection(date)
    timee = await date_collection.insert_one(time_data)
    new_timee = await date_collection.find_one({"_id": timee.inserted_id})
    print("added date"+date+"and "+str(time_data["time"]))
    return twod_helper(new_timee)

async def add_new_collection_start_the_day(date:str, time_data:dict)->dict:
    create_a_collection = await database.create_collection(date)

    date_collection = database.get_collection(date)
    timee = await date_collection.insert_one(time_data)
    new_timee = await date_collection.find_one({"_id": timee.inserted_id})
    print("added date"+date+"and "+str(time_data["time"]))
    return twod_helper(new_timee)

async def remove_collection():
    all_collections = await database.list_collection_names(filter=None)
    for collect in all_collections:
        #print(collect)
        lst =  str(collect).split("-")
        date = datetime(int(lst[2]),int(lst[1]),int(lst[0]))
        past30Days = datetime.now() - timedelta(days=31)
        if(date<past30Days):
            print("drop this collection = "+str(collect))
            database.drop_collection(collect)
    

