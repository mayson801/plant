import schedule
import time
from plant_tweet import *
from  pringle_tweet import *

if __name__ == '__main__':
    #schedule.every().day.at("07:00").do(water_tweet)
    #schedule.every().day.at("19:00").do(water_tweet)

    schedule.every().day.at("08:00").do(create_pringal_tweet)
    while True:
        schedule.run_all()
        #schedule.run_pending()
        time.sleep(1)
