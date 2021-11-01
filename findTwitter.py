from datetime import datetime
import requests
from bs4 import BeautifulSoup
import feedparser
import os
#import re, os, lib, sys
#import urllib.request

def storyInfo(entry, number):
    """Returns list with the title, and date  of the given entry"""
    story_title = entry.title
    date = entry.published.split()
    date = date[1:4]
    #date.reverse()
    date = "-".join(str(x) for x in date)
    date = datetime.strptime(date, '%d-%b-%Y')
    date = date.strftime('%Y-%m-%d')
    story_date = date
    storyurl = entry.link
    return story_title, story_date, storyurl

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
        if twitterS == []:
            twitterS.extend(twitter_B(x))
        story_twitter.append(twitterS)
    twitter_list = []
    for l in story_twitter:
        for item in l:
            item = item.lower()
            twitter_list.append(item)
    #twitter_list = list(set(twitter_list)) 
    #twitter_list = checkReal(twitter_list)
    return twitter_list

def checkReal(twitter_list):
    #twitters = []
    for handle in twitter_list:
        twitter_link = 'https://twitter.com/'+handle
        try:
            GrepBeatFeed = feedparser.parse(twitter_link)
            #twitters.append(handle)
        except:
            twitter_list.remove(handle)
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
                allLinkList = allLink.replace('?', '/').replace('\\', '/').split('/') #.replace('\'', '_').replace('.', '_')
                index_of_handle = allLinkList.index(substring) + 1
                handle = allLinkList[index_of_handle]
                if handle not in twitterS:
                    twitterS.append(handle)
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
                handle_index = handle.index(subtring) + 1
                handle = handle[handle_index]
                if handle not in twitterS:
                    twitterS.append(handle)
        return twitterS
    except:
        return twitterS
