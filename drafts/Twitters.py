import mysql.connector
from datetime import datetime
import os
import requests
from bs4 import BeautifulSoup
import feedparser
import re

import sys
sys.path.append('/home/ximena/auth')
import authTS

mydb = mysql.connector.connect(host=authTS.HOSTNAME, user=authTS.USERNAME, password=authTS.PASSWORD)
mycursor = mydb.cursor()
db_statement = "use {}".format(authTS.DATABASE)
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
        urls = Links(entry)
        twitters = findTwitter(urls)
        insertTwitters(story_info, twitters)
        #print(urls)
        #print(twitters)
        #print(type(story_info))
        #print(story_info)
        i-=1


def storyInfo(entry, number):
    """Returns list with the #, title, and date  of the given entry"""
    story_title = entry.title
    date = entry.published.split()
    date = date[1:4]
    #date.reverse()
    date = "-".join(str(x) for x in date)
    date = datetime.strptime(date, '%d-%b-%Y')
    date = date.strftime('%Y-%m-%d')
    story_date = date
    return story_title, story_date

def insertStoryInfo(info):
    sql = "select MAX(story_id) from Stories"
    mycursor.execute(sql)
    story_number = mycursor.fetchall()
    story_number = story_number[0]
    story_number = story_number[0]
    story_number = str(story_number+1)
    #story_id = int(info[0])
    title = info[1]
    date = info[2]
    print(story_id, title, date)
    print("")
    query = "insert ignore into Stories(story_id, title, date) values(%s, %s, %s)"
    args = (story_number, title, date)
    mycursor.execute(query, args)
    mydb.commit()

def insertTwitters(info, twitters):
    sql = "select MAX(handle_id) from Handles"
    mycursor.execute(sql)
    handle_number = mycursor.fetchall()
    handle_number = handle_number[0]
    handle_number = handle_number[0]
    handle_number = handle_number+1
    title = info[1]
    sql2 = "SELECT story_id FROM Stories WHERE title = %s"
    args = (title, )
    mycursor.execute(sql2, args) 
    story_id = mycursor.fetchall()
    #print(story_id)
    story_id = story_id[0]
    story_id = story_id[0]
    print(story_id)
    print(type(story_id))
    for handle in twitters:
        sql3 = "select EXISTS(select * from bad_handles where handle = %s)"
        args3 = (handle, )
        mycursor.execute(sql3, args3)
        bad_handle = mycursor.fetchall()
        bad_handle = bad_handle[0]
        bad_handle = bad_handle[0]
        if bad_handle == 0:
            sql4 = "insert ignore into Handles(handle_id, story_id, handle) values(%s, %s, %s)"
            args4 = (int(handle_number), int(story_id), handle)
            mycursor.execute(sql4, args4)
            mydb.commit()


def Links(entry):
    """Returns list with all the urls in an entry"""
    urls = []
    soup = BeautifulSoup(str(entry.content), features="html.parser")
    for a in soup.find_all('a', href=True):
        url = a['href']
        url = url.split('/')
        url = url[:3]
        url = '/'.join(url)
        urls.append(url)
    Urls = []
    for i in urls: 
        if i not in Urls: 
            Urls.append(i) 
    return Urls

def findTwitter(urls):
    """Takes list of links and returns a list the twitters"""
    story_twitter = []
    for x in urls:
        twitterS = twitter_A(x)
        if twitter_B(x) != twitter_A(x):
            twitterS.extend(twitter_B(x))
        story_twitter.append(twitterS)
    twitter_list = []
    for l in story_twitter:
        for item in l:
            twitter_list.append(item)
    return twitter_list


def twitter_A(link):
    """One method to get a list of twitter handles for a link"""
    twitterS = []
    substring = 'twitter.com'
    try:
        res = requests.get(str(link), timeout=10)
        otherSoup = BeautifulSoup(str(res.text), features="html.parser")
        for a in otherSoup.find_all('a', href=True):
            allLink = a['href']
            if substring in allLink:
                allLinkList = allLink.replace('?', '').replace('\\', '').split('')
                if allLinkList[3] not in twitterS:
                    twitterS.append(allLinkList[3])
            #allLinkList = allLink.split('/')
            #if len(allLinkList) > 2 and allLinkList[2] == 'twitter.com':
            #    twitterS.append(allLinkList[3])
        return twitterS
    except:
        return twitterS

def twitter_B(link):
    """Another method to get a list of handles for a link"""
    twitterS = []
    try:
        substring = 'twitter.com'
        c = 'curl -s '
        command = c+link
        #result = os.popen(command,stdout=open(os.devnull, 'wb')).read()
        result = os.popen(command).read()
        result = result.replace('&quot;', '"').replace("'", '"').replace("?", '"').split('"')
        for i in result:
            if substring in i:
                handle = i.split('/')
                handle = handle[3]
                if handle not in twitterS:
                    twitterS.append(handle)
        return twitterS
    except:
        return twitterS


if __name__ == "__main__":
    main()
           
