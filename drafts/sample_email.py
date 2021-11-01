#importing the Yagmail library
import yagmail
from datetime import date

cur_date = date.today()
to='ximena@grepbeat.com'
subject='Sample email using yagmail({})'.format(cur_date)
contents='I am going to practice counting with indentation:'
bullet_point = u'\u2022'

i=1
while (i<10):
    contents += "\n\t{} {}".format(bullet_point, i)
    i+=1

contents += "Here I am going to try indenting with just spaces"
i=1
while (i<10):
    contents += "\n    {} {}".format(bullet_point, i)
    i+=1
print(contents)

try:
    #initializing the server connection
    yag = yagmail.SMTP(user='ximenabotbot@gmail.com', password='Twitterbot')
    #sending the email
    yag.send(to=to , subject=subject, contents=contents)
except:
    print("Error, email was not sent")

