import feedparser
from datetime import datetime
import mysql.connector

import sys
sys.path.append('/home/ximena/auth')
import authTS

mydb = mysql.connector.connect(host=authTS.HOSTNAME, user=authTS.USERNAME, password=authTS.PASSWORD)
mycursor = mydb.cursor()
db_statement = "use {}".format(authTS.DATABASE)
mycursor.execute(db_statement)

def findLinks(NewsFeed):
    i = 0 
    while i < len(NewsFeed.entries):
        #print ('Story #',i+1)
        entry = NewsFeed.entries[i]
        date = entry.published.split()
        date = date[1:4]
    #date.reverse()
        date = "-".join(str(x) for x in date)
        date = datetime.strptime(date, '%d-%b-%Y')
        date = date.strftime('%Y-%m-%d')

        #mycursor.execute("INSERT INTO Stories(title, date) VALUES ('%s', STR_TO_DATE('%s', '%%d %%b,%%Y'))" % (title, date))
        print(type(date))
        print(date)
        i+=1

GrepBeatFeed = feedparser.parse('https://grepbeat.com/feed/')
findLinks(GrepBeatFeed)
