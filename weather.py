# -*- coding: utf-8 -*-
"""
Created on Fri Dec 16 15:32:28 2016

@author: kilicm
"""




import json
import requests
import os
import tweepy
import time

# == OAuth Authentication ==
#
# This mode of authentication is the new preferred way
# of authenticating with Twitter.

# The consumer keys can be found on your application's Details
# page located at https://dev.twitter.com/apps (under "OAuth settings")

## The access tokens can be found on your applications's Details
## page located at https://dev.twitter.com/apps (located
## under "Your access token")

with open('mycreds.json') as json_data:
    my_credentials = json.load(json_data)
   
    
consumer_key = my_credentials['mycreds']['twitterapi']['consumer_key']
consumer_secret = my_credentials['mycreds']['twitterapi']['consumer_secret']

access_token = my_credentials['mycreds']['twitterapi']['access_token']
access_token_secret = my_credentials['mycreds']['twitterapi']['access_token_secret']

weather_api = my_credentials['mycreds']['weatherapi']['apiid']


auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth)



# If the authentication was successful, you should
# see the name of the account print out
print(api.me().name)

# If the application settings are set for "Read and Write" then
# this line should tweet out the message to your account's
# timeline. The "Read and Write" setting is on https://dev.twitter.com/apps




def get_weather_json(city):
    req = requests.get("http://api.openweathermap.org/data/2.5/weather?q={}&units=imperial&appid={}".format(city, weather_api))
    return req.json()
    

    
def get_weather_icon():
    description = get_weather_json(city)['weather'][0]['description']
    fn =  os.path.abspath("/Users/kilicm/Desktop/Python Examples/icons")
    
    icon = ''
    if description == 'clear sky':
        icon =  fn + '/01d.png'
    elif description == 'few clouds':
        icon = fn + '/02d.png'
    elif description == 'scattered clouds':
        icon = fn + '/03d.png'    
    elif description in ['broken clouds','overcast clouds']:
        icon = fn + '/04d.png'    
    elif description in ['light intensity drizzle','drizzle','heavy intensity drizzle','light intensity drizzle rain','drizzle rain','heavy intensity drizzle rain','shower rain and drizzle','heavy shower rain and drizzle','shower drizzle','light intensity shower rain','shower rain','	heavy intensity shower rain','ragged shower rain']:
        icon = fn + '/09d.png'    
    elif description in ['light rain','moderate rain','heavy intensity rain','very heavy rain', 'extreme rain']:
        icon = fn + '/10d.png'    
    elif description in  ['thunderstorm with light rain','thunderstorm with rain','thunderstorm with heavy rain','light thunderstorm','thunderstorm','heavy thunderstorm','ragged thunderstorm','thunderstorm with light drizzle','thunderstorm with drizzle','thunderstorm with heavy drizzle']:
        icon = fn + '/11d.png'
    elif description in  ['light snow','snow','heavy snow','sleet','shower sleet','light rain and snow','rain and snow','light shower snow','shower snow','heavy shower snow','freezing rain']:
        icon = fn + '/13d.png'
    elif description in ['mist','smoke','haze',"sand, dust whirls",'fog','sand','dust','volcanic ash','squalls','tornado']:
        icon =  fn + '/50d.png'
    return icon
 
   
def get_weather_description():
    return get_weather_json(city)['weather'][0]['description']
    

if __name__ == '__main__':

    while True:
        try:
        
            tweets = api.search('weather today', geocode="39.8,-95.583068847656,2500km", count=10, lang="en")
        except tweepy.RateLimitError:
            time.sleep(6000*15)
            continue
        
        for tweet in tweets :
            username = tweet.user.screen_name
            user_id = tweet.id
            text = tweet.text
            city = tweet.user.location
            print("User tweet is {}".format(text))
            print("User name is @{}".format(username))
            print("User city is {}".format(city))
            print(".................................")
            tbaglanti = "https://twitter.com/{}/status/{}".format(username, user_id)
            
        
            
            try:   
                current_weather, temp_max, temp_min = [get_weather_json(city)['main'][i] for i in ['temp', 'temp_max', 'temp_min']]
            except KeyError:
                break
                
            pri = ('{} @{} Weather: Currently {} & {:.0f}°F. Expect a high of {:.0f}°F and a low of {:.0f}°F.'.format(tbaglanti, username, get_weather_description(), current_weather,temp_max, temp_min))
            print (pri)
            api.update_with_media(get_weather_icon(), status=pri)
            time.sleep(30000)
            
            
        
# 
