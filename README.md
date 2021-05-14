# POST_DATABASE_AUTOMATIC_SCRIPT

A Python Script which posts 10x10 2D random numpy array with random elements on the MongoDB Database everyday.
Cron Job is used to schedule task like it will only post everyday from 8 am IST to 9:30 pm IST.
Everyday when the day starts this python script creates a new collection at my database and then creates numerous documents for various time as mentioned above.

I have used ASYNCIOScheduler of APscheduler.

It also removes old collection like the collection that were created 30 days before.


## Format of the Document on MongoDB Collection:

{
"time": <Time in String> \n
"twod_data": <A 2D array> \n
"fourd_data": <A 2D array with gaps at random places> \n
  }
