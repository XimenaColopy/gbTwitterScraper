import feedparser
from datetime import datetime
import mysql.connector

mydb = mysql.connector.connect(host="localhost", user="ximena", password="Horse4horse")
mycursor = mydb.cursor()

db_statement = "use ximenabot"
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
