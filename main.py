import requests
import sqlite3
connection=sqlite3.connect('previous')
cursor=connection.cursor()
import time
import subprocess
import os
import signal
from discord_hooks import Webhook
from html.parser import HTMLParser
parser = HTMLParser()
url="https://discordapp.com/api/webhooks/487006022729334814/_y9zHMUlUP4eOLBHDrZOHrc8ZU3lBdRh_J-CyH3abawinNfu6ZjjrWV3FWRkmpnNosEp"
cursor.execute('''CREATE TABLE IF NOT EXISTS news(
    name text,
    title text,
    content text,
    link varchar(255),
    picture varchar(255)
)''')
connection.commit()
while True:
    try:
        a=(requests.get('https://coinhooked.com/wp-admin/admin-ajax.php?action=fetch_posts&stream-id=1&disable-cache=',headers={'_gat':'1'}))
    except:
        time.sleep(60)
        continue
    a=(a.json())
    a=a['items'][0]

    name=a['screenname']
    if name=='Cointelegraph':
        picture='https://cointelegraph.com/assets/img/logo.png'
    else:
        picture=a['userpic'].replace('\\/','/')

    title=a['header']
    content=a['text']
    link=a['permalink']
    if 'This is a paid-for submitted press release.' not in content:
        cursor.execute('''SELECT * FROM news where link="%s"'''%(link))
        if len(cursor.fetchall())==0:
            cursor.execute('''DELETE FROM news where link=(SELECT link from news)''')
            cursor.execute('''INSERT INTO news VALUES(
            "%s",
            "%s",
            "%s",
            "%s",
            "%s")
            '''%(name,title,content,link,picture))
            connection.commit()
            embed = Webhook(url, color=0x505358)
            embed.set_author(name=name, icon=picture)
            embed.set_title(title=title,url=link)
            embed.set_desc(parser.unescape(content.replace('<br>','')))
            embed.post()
