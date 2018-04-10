import os
import asyncio
import telepot
import telepot.aio
from random import randint
import praw
import json
from telepot.aio.loop import MessageLoop
#from urllib.request import urlopen

TELEGRAM = os.environ['RG_TELEGRAM_TOKEN']
CLIENT_ID = os.environ['RG_REDDIT_CLIENT_ID']
CLIENT_SECRET = os.environ['RG_REDDIT_CLIENT_SECRET']
USERNAME = os.environ['RG_REDDIT_USERNAME']
PASSWORD = os.environ['RG_REDDIT_PASSWORD']

#print('{}\n{}\n{}\n{}\n{}'.format(TELEGRAM,CLIENT_ID,CLIENT_SECRET,USERNAME,PASSWORD))

def load_json():
    with open('subs.json') as db:
        global sublist
        sublist = json.load(db)

def add_sub(local_list, subname, subtype):
    local_list['subs'].append({"path":subname,"type":subtype})
    with open('subs.json', 'w') as db:
        json.dump(local_list, db, indent=2)
    load_json()

load_json()

reddit = praw.Reddit(client_id=CLIENT_ID,
                     client_secret=CLIENT_SECRET, password=PASSWORD,
                     user_agent='RedGiffer', username=USERNAME)

async def handle(msg):
    chat_id = msg['chat']['id']
    command = msg['text'].split()[0]

    if command == '/get':
        sub = reddit.subreddit(sublist['subs'][randint(0,len(sublist['subs'])-1)]['path'])
        post = sub.random()
        await bot.sendMessage(chat_id, 'Sub: /r/{}\nPost ID: {}'.format(sub.display_name, post))
        await bot.sendMessage(chat_id, post.url)

    elif command == '/sub':
        if (len(msg['text'].split()) > 1):
            s2 = reddit.subreddit(msg['text'].split()[1]).random()
            await bot.sendMessage(chat_id, s2.url)
        else:
            await bot.sendMessage(chat_id, 'Missing sub name')

    elif command == '/reload':
        load_json()
        await bot.sendMessage(chat_id, 'JSON Reloaded!')

    elif command == '/add':
        if (len(msg['text'].split()) > 2):
            add_sub(sublist, msg['text'].split()[1], msg['text'].split()[2])
        else:
            await bot.sendMessage(chat_id, 'You need 2 parameters')
    
bot = telepot.aio.Bot(TELEGRAM)
loop = asyncio.get_event_loop()

loop.create_task(MessageLoop(bot, handle).run_forever())
print('Listening ...')

loop.run_forever()

