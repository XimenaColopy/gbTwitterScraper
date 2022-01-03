
### Lowkey I have no idea what this is. I'm pretty sure I just copied this from the internet. I doubt it works 
### It does look cool tho...


# TAKE HANDLES AND CONVERT TO USERID COMMA SEPARATED
 
import tweepy
#import csv
import time
 
# GLOBAL VARS
consumer_key = 'CREATE_AND_INSERT'
consumer_secret = 'CREATE_AND_INSERT'
access_token = 'CREATE_AND_INSERT'
access_token_secret = 'CREATE_AND_INSERT'
 
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
 
# SET OBJECT AND AUTHENTICATE
api = tweepy.API(auth)
 
# Prompt for usernames
print('Format input like this username1,username2,username3')
 
myHandles = input("Feed a comma separated list of user handles without the @-precursor ")
 
#Check for valid input
if myHandles:
    # Clear the input, prepare for lookup
    myHandles = myHandles.lower()
    myHandles = myHandles.replace('@','')
    myHandles = myHandles.replace(' ','')
    myHandles = myHandles.split(',')
    # Set a new list object
    myIdList = []
    i = 0
    # Loop trough the list of usernames
    for handle in myHandles:
        u = api.get_user(myHandles[i])
        uid = u.id
        myIdList.append(uid)
        i = i+1
        print(i)
    # Print the lists
    print('Usernames',myHandles)
    print('Twitter-Ids',myIdList)
    #set a filename based on current time
   # csvfilename = "csvoutput-"+time.strftime("%Y%m%d%-H%M%S")+".csv"
   # print('We also outputted a CSV-file named '+csvfilename+' to your file parent directory')
   # with open(csvfilename, 'w') as myfile:
   #     wr = csv.writer(myfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
   #     wr.writerow(['username','twitter-id'])
   #     j = 0
   #     for handle in myHandles:
   #         writeline = myHandles[j],myIdList[j]
   #         wr.writerow(writeline)
   #         j = j+1
else:
    print('The input was empty')
