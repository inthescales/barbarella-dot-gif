import random
import os
import ConfigParser
import time
import subprocess

from tumblpy import Tumblpy
from makeGifs import makeGif, check_config

config = ConfigParser.ConfigParser()
config.read("config.cfg")
config.sections()
slugs = check_config("config.cfg")[3]

CONSUMER_KEY = config.get("tumblr", "consumer_key")
CONSUMER_SECRET = config.get("tumblr", "consumer_secret")
OAUTH_TOKEN = config.get("tumblr", "oauth_token")
OAUTH_TOKEN_SECRET = config.get("tumblr", "oauth_token_secret")


t = Tumblpy(
    CONSUMER_KEY,
    CONSUMER_SECRET,
    OAUTH_TOKEN,
    OAUTH_TOKEN_SECRET,
)

while True:
    # you can set many more options, check the makeGif-function
    quote = makeGif(random.choice(slug), frames=20)
    quote = ' '.join(quote)

    # reduce amount of colors, because tumblr sucks
    subprocess.call(['convert',
                     'barbarella.gif',
                     '-layers',
                     'optimize',
                     '-colors',
                     '64',
                     '-loop',
                     '0',
                     'barbarella.gif'])

    while(os.path.getsize('barbarella.gif') > 1048576):
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

    photo = open('barbarella.gif', 'rb')

    post = t.post(
        'post',
        #blog_url='http://barbarellagifs.tumblr.com',
        params={
            'type': 'photo',
            'caption': quote,
            'data': photo,
            'tags': 'barbarella, gif'}
    )

    print "sleeping..."
    # sleep 12 hours
    time.sleep(43200)
