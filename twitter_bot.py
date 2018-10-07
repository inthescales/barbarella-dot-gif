import base64
import json
import requests
import configparser
import random
import os
import time
import subprocess

from twython import Twython
from base64 import b64encode
from makeGifs import makeGif, check_config


config = configparser.ConfigParser()
config.read("config.cfg")
config.sections()
slugs = check_config("config.cfg")[3]

APP_KEY = config.get("twitter", "app_key")
APP_SECRET = config.get("twitter", "app_secret")
OAUTH_TOKEN = config.get("twitter", "oauth_token")
OAUTH_TOKEN_SECRET = config.get("twitter", "oauth_token_secret")

while True:
    while True:
        try:
            # you can set many more options, check the makeGif-function
            quote = makeGif(random.choice(slugs))
            quote = ' '.join(quote)
        except:
            print('something went wrong during gif-generation')
            continue
        else:
            break

    # first pass reduce the amount of colors
    if(os.path.getsize('barbarella.gif') > 5242880):
        subprocess.call(['convert',
                         'barbarella.gif',
                         '-layers',
                         'optimize',
                         '-colors',
                         '128',
                         '-loop',
                         '0',
                         'barbarella.gif'])

    # second pass reduce the amount of colors
    if(os.path.getsize('barbarella.gif') > 5242880):
        subprocess.call(['convert',
                         'barbarella.gif',
                         '-layers',
                         'optimize',
                         '-colors',
                         '64',
                         '-loop',
                         '0',
                         'barbarella.gif'])

    # other passes reduce the size
    while(os.path.getsize('barbarella.gif') > 5242880):
        subprocess.call(['convert',
                         'barbarella.gif',
                         '-resize',
                         '90%',
                         '-coalesce',
                         '-layers',
                         'optimize',
                         '-loop',
                         '0',
                         'barbarella.gif'])

    twitter = Twython(APP_KEY, APP_SECRET, OAUTH_TOKEN, OAUTH_TOKEN_SECRET)

    # upload media
    gif = open('barbarella.gif', 'rb')
    response = twitter.upload_media(media=gif)

    if len(quote) > 70:
        quote = (quote[:67] + '...')

    if len(quote) == 0:
        quote = "..."

    status = quote

    print("tweeting...")
    try:
        twitter.update_status(status=status, media_ids=[response['media_id']])
    except:
        # error with twitter sleep a bit and try again
        time.sleep(1800)
        continue

    print("sleeping...")
    # sleep 2 hours
    time.sleep(7200)
    #time.sleep(3600)
