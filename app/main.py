from datetime import datetime,timedelta,timezone
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from twoD_database import *
import asyncio
from numpy.random import default_rng
import numpy as np
import os
import time
import random as r
import copy
import random
os.environ['TZ'] = 'Asia/Kolkata' # set new timezone
time.tzset()

isSeventify = True 

def ceil_dt(dt, delta):
    return dt + (datetime.min - dt) % delta

def spreadRandom(theRange, howMany, minSpacing):
    while True:
        candidate = sorted([r.randint(*theRange) for _ in range(howMany)])
        minDiff = min([ candidate[i+1]-candidate[i] for i, _ in enumerate(candidate[:-1])])
        if minDiff >= minSpacing:
            return candidate

def generate_random_array(size):
    rng = default_rng()
    numbers = rng.choice(100, size=size, replace=False)
    numbersList = numbers.tolist()
    sampledList = random.sample(numbersList, 100-size)
    numbersList = numbersList + sampledList
    random.shuffle(numbersList)
    numberArray = np.array(numbersList).reshape(10,10,1)
    return numberArray.tolist()


def deleteAndswap(array,elementindex,replaceIndex):
  string_ele =str(elementindex).zfill(2)
  string_rep = str(replaceIndex).zfill(2)
  ele=array[int(string_ele[0])][int(string_ele[1])][0]
  #print("ele is",ele)
  array[int(string_ele[0])][int(string_ele[1])].clear()
  array[int(string_rep[0])][int(string_rep[1])].append(ele)

def fourd_generator(numbersList):
    randomIndex = spreadRandom([0,99],10,3)
    #print("random Index is ",randomIndex)
    diff = [-1,+1,-1,+1,-1,+1,-1,+1,-1,+1]
    for i in range(len(randomIndex)):
        item = randomIndex[i]
        if(str(item).zfill(2)[1]=='0'):
            ##print("0th part")
            deleteAndswap(numbersList,item,item+1)
        elif(str(item).zfill(2)[1]=='9'):
            ##print("9th part")
            deleteAndswap(numbersList,item,item-1)
        else:
            deleteAndswap(numbersList,item,item+diff[i])
    return numbersList    


async def add_to_database():
    next_time=ceil_dt(datetime.now(),timedelta(minutes=15))
    next_time=str(next_time.hour).zfill(2)+str(next_time.minute).zfill(2)
    global isSeventify
    if(isSeventify):
        #print(isSeventify)
        twod_value= generate_random_array(75)
    else: 
        #print(isSeventify)
        twod_value = generate_random_array(80)
    isSeventify = not isSeventify    
    temp_twod = copy.deepcopy(twod_value)
    fourd_value = fourd_generator(temp_twod)
    data_dict={
        "time": next_time,
        "twod_value": twod_value,
        "fourd_value": fourd_value
        }
    #print("uploading Data"+str(data_dict))
    today_date = str(datetime.now().day).zfill(2)+"-"+str(datetime.now().month).zfill(2)+"-"+str(datetime.now().year)    
    new_twod_data = await add_time(today_date,data_dict)
    #print("added successfully"+str(new_twod_data))

async def add_new_day():
    next_time=ceil_dt(datetime.now(),timedelta(minutes=15))
    next_time=str(next_time.hour).zfill(2)+str(next_time.minute).zfill(2)
    global isSeventify
    if(isSeventify):
        #print(isSeventify)
        twod_value= generate_random_array(75)
    else: 
        #print(isSeventify)
        twod_value = generate_random_array(80)
    isSeventify = not isSeventify   
    temp_twod = copy.deepcopy(twod_value)
    fourd_value = fourd_generator(temp_twod)
    data_dict={
        "time": next_time,
        "twod_value": twod_value,
        "fourd_value": fourd_value
        }
    today_date = str(datetime.now().day).zfill(2)+"-"+str(datetime.now().month).zfill(2)+"-"+str(datetime.now().year)
    new_twod_data = await add_new_collection_start_the_day(today_date,data_dict)
    #print("added successfully"+str(new_twod_data))


async def end_the_day():
    next_time=ceil_dt(datetime.now(),timedelta(minutes=15))
    next_time=str(next_time.hour).zfill(2)+str(next_time.minute).zfill(2)
    global isSeventify
    if(isSeventify):
        #print(isSeventify)
        twod_value= generate_random_array(75)
    else: 
        #print(isSeventify)
        twod_value = generate_random_array(80)
    isSeventify = not isSeventify
    temp_twod = copy.deepcopy(twod_value)
    fourd_value = fourd_generator(temp_twod)
    data_dict={
        "time": next_time,
        "twod_value": twod_value,
        "fourd_value": fourd_value
        }
   # #print("uploading Data"+str(data_dict))
    today_date = str(datetime.now().day).zfill(2)+"-"+str(datetime.now().month).zfill(2)+"-"+str(datetime.now().year)
    new_twod_data = await add_time(today_date,data_dict)
    #print("added successfully"+str(new_twod_data))

async def remove_old_data():
    remove_collection()


if __name__ =="__main__":
    #print(datetime.now())
    scheduler = AsyncIOScheduler()
    scheduler.add_job(add_to_database,'cron',hour='8-20',minute="5,20,35,50")
    scheduler.add_job(add_new_day,'cron',hour='7',minute='50')
    scheduler.add_job(end_the_day,'cron',hour='21',minute='5,20')
    scheduler.add_job(remove_old_data,'cron',hour="0",minute="0")
    scheduler.start()
    asyncio.get_event_loop().run_forever()





