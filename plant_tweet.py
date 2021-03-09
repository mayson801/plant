import random
import json
import os
import tweeter

#this will only work on pi
#from board import SCL, SDA
#import busio
#from adafruit_seesaw.seesaw import Seesaw


def tweet_generator(number):
    if (number<1000):
        no1 = (random.randint(0, 9))
        no2 = (random.randint(0, 9))
        no3 = (random.randint(0, 9))
        no4 = (random.randint(0, 9))

        #print(str(no1) + " " +str(no2) + " "+ str(no3) +" " + str(no4))
        cwd = os.getcwd()
        with open(cwd+'\data.json') as json_file:
            data = json.load(json_file)
        tweet = data["bad_intro"][no1]+data["insult"][no2]+data["say_plant_needs_water"][no3]+data["outro"][no4]+ "\nwater leval=" + str(number)
        return tweet
def water_sensor():
    #this will only work on pi
    #i2c_bus = busio.I2C(SCL, SDA)
    #ss = Seesaw(i2c_bus, addr=0x36)

    #moisture_value = ss.moisture_read()

    moisture_value = 500
    return moisture_value

def water_tweet():
    water_value = water_sensor()
    tweet_text = tweet_generator(water_value)
    #tweeter.tweet(tweet_text)
    print(tweet_text)

water_tweet()