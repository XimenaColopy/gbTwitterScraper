#import mysql.connector
#from datetime import datetime, date
#import os
#import requests
#from bs4 import BeautifulSoup
import feedparser
#import re
#import yagmail

from findTwitter import storyInfo, Links, findTwitter, twitter_A, twitter_B
from add_to_database import insertStoryInfo, insertTwitters, insertIntoIntersect, closeGap, retrieveTwitters
from send_twittermail import sendEmail



#get rid of autoincrementing bug
closeGap('Stories')
closeGap('Handles')


GrepBeatFeed = feedparser.parse('https://grepbeat.com/feed/')
#exit

i = len(GrepBeatFeed.entries)-1 #should be 9
email_content = []
while i >= 0:
    new_content = []
    entry = GrepBeatFeed.entries[i]
    story_info = storyInfo(entry, i)
    new_story_info = insertStoryInfo(story_info) #returns none if the story is already in the database
    print('\nStory:')
    if new_story_info != None:
        print(new_story_info)
        urls = Links(entry)
        twitters = findTwitter(urls)
        #print('\nTwitters found')
        #for x in twitters: print(x)
        new_handles = insertTwitters(story_info, twitters)
        print('Added twitters:')
        for x in new_handles: print(x)
        insertIntoIntersect(twitters, story_info)

        new_content.append(retrieveTwitters(new_story_info[0]))
        new_content = list(filter(None, new_content)) #remove the None values
        if new_content != []:
            new_content.append(new_story_info[0])
            new_content.append(new_story_info[1])
            new_content.append(new_story_info[2])
        #print(new_content)

    email_content.append(new_content)
    i-=1

email_content = [x for x in email_content if x != []]
#if email_content != []:
#    sendEmail(email_content, date.today())
print(email_content)
   


