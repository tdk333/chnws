import requests
import sqlite3
import random
from html.parser import HTMLParser
parser = HTMLParser()
connection=sqlite3.connect('previous')
cursor=connection.cursor()

import sys
import json
import discord
from discord.ext import commands
import time
TOKEN = 'NDQwOTMzMjE1NTc5MTQ0MjAz.DmWipQ.p110Y5lhaNCZMYiDYI8mNtghNpk'

description = '''ninjaBot in Python'''
bot = commands.Bot(command_prefix='?', description=description)
client=discord.Client()
prev=''

@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')
    prev=''
    while True:
        cursor.execute('''SELECT * FROM news''')
        a=cursor.fetchall()[0]
        name=a[0]
        title=a[1]
        content=a[2]
        link=a[3]
        picture=a[4]
        if link!=prev:
            prev=link
            for server in bot.servers:
                for channel in server.channels:
                    if 'text' in str(channel.type) and str(channel.name).lower() == 'news':
                        embed = discord.Embed(title=title,description=parser.unescape(content.replace('<br>','')),url=link)

                        embed.set_author(name=name,icon_url=picture)
                        await bot.send_message(channel, embed=embed)




bot.run(TOKEN)