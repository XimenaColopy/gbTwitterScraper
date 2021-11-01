import mysql.connector 
from datetime import datetime
import os
import requests
from bs4 import BeautifulSoup
import feedparser
import re

mydb = mysql.connector.connect(host="localhost", user="ximena", password="Horse4horse")
mycursor = mydb.cursor()
db_statement = "use ximenabot"
mycursor.execute(db_statement)
#mycon = mysql.connector.connect(
#    host='localhost',
#    user='ximena',
#    password='Horse4Horse', 
#    database='ximenabot '
#)
#mycursor = mycon.cursor()

#story info is a tuple with the #, title, and date
def main() -> None:
    GrepBeatFeed = feedparser.parse('https://grepbeat.com/feed/')
    i = len(GrepBeatFeed.entries)-1 #should be 9
    while i >= 0:
        entry = GrepBeatFeed.entries[i]
        story_info = storyInfo(entry, i)
        insertStoryInfo(story_info)
        #print(type(story_info))
        #print(story_info)
        i-=1


def storyInfo(entry, number):
    """Returns list with the #, title, and date  of the given entry"""
    #sql = "select story_id from Stories ORDER BY story_id DESC LIMIT 1"
    sql = "select MAX(story_id) from Stories"
    mycursor.execute(sql)
    story_number = mycursor.fetchall()
    story_number = story_number[0]
    story_number = story_number[0]
    story_number = str(story_number+1)
    story_title = entry.title
    date = entry.published.split()
    date = date[1:4]
    #date.reverse()
    date = "-".join(str(x) for x in date)
    date = datetime.strptime(date, '%d-%b-%Y')
    date = date.strftime('%Y-%m-%d')
    story_date = date
    return story_number, story_title, story_date


def insertStoryInfo(info):
    story_id = int(info[0])
    title = info[1]
    date = info[2]
    print(story_id, title, date)
    print("")
    query = "insert ignore into Stories(story_id, title, date) values(%s, %s, %s)"
#    query = "INSERT INTO stories(story_name, story_date) " \
#            "VALUES(%s,%s)"
    args = (story_id, title, date)
    mycursor.execute(query, args)
    mydb.commit()

if __name__ == "__main__":
    main()
