#importing the Yagmail library
import yagmail
from datetime import date

def sendEmail(info, cur_date):
    #to='pete@grepbeat.com'
    to='jackie@grepbeat.com'
    #to='ximena@grepbeat.com'
    subject='GrepBeat Twitter Finder for {}'.format(cur_date)
    contents='Here are the new stories with their Twitter handles:'
    bullet_point = u'\u2022'
    for story in info:
        twitters = story[0]
        title = story[1]
        date = story[2]
        storyurl = story[3]
        line = "\n\n{} ({})".format(title, date)
        contents += line
        line = "\n{}".format(storyurl)
        contents += line
        for handle in twitters:
            twitterurl = 'https://twitter.com/'+handle
            line = "\n {} {} {} {}".format(bullet_point, bullet_point, bullet_point, twitterurl)
            contents += line

    line = "\nEnjoy! \nGrepBeat Twitter Fairy"
    contents += line 
    try:
        #initializing the server connection
        yag = yagmail.SMTP(user={'ximenabotbot@gmail.com': "GrepBeat Twitter Fairy"}, password='Twitterbot')
        #sending the email
        yag.send(to=to , subject=subject, contents=contents)
        #yagmail.SMTP({"user@gmail.com": "Alias"}, "pwd").send(mail, subject, body)
    except:
        print("Error, email was not sent")

