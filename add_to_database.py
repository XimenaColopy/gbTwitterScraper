import mysql.connector
import feedparser
import re
import sys

sys.path.append('/home/ximena/auth')
import authTS

mydb = mysql.connector.connect(host=authTS.HOSTNAME, user=authTS.USERNAME, password=authTS.PASSWORD)
mycursor = mydb.cursor()
db_statement = "use {}".format(authTS.DATABASE)
mycursor.execute(db_statement)


def retrieveTwitters(title):
    """Returns all the twitters associated with a story"""
    twitters = []
    sql = "select story_id from Stories where title = %s"
    args = (title, )
    mycursor.execute(sql, args)
    s_id = mycursor.fetchall()[0][0]
    #Id = Id[0]
    #Id = Id[0]

    sql = 'select handle_id from Intersect where story_id = %s'
    args = (s_id, )
    mycursor.execute(sql, args)
    h_id = mycursor.fetchall()
    try:
        h_id = list(zip(*h_id))[0]
        #print('list of handle id:', hid)
        sql = 'select handle from Handles where handle_id = %s'
        for i in h_id:
            args = (i, )
            mycursor.execute(sql, args)
            handle = mycursor.fetchall()
            handle = list(zip(*handle))[0][0]
            twitters.append(handle)
    finally:
        return twitters


def insertStoryInfo(info):
    title = info[0]
    title = title.lower()
    if not testIfItemExists("Stories", title):
        date = info[1]
        url = info[2]
        sql = "insert into Stories(title, date, story_url) values(%s, %s, %s)"
        args = (title, date, url)
        mycursor.execute(sql, args)
        mydb.commit()
        return title, date, url


def insertTwitters(info, twitters):
    title = info[0]
    handles = []
    for handle in twitters:
        bad_handle = check_if_bad(handle)
        if bad_handle == 0:
            if not testIfItemExists("Handles", handle):
                sql = "insert into Handles(handle) values(%s)"
                args = (handle, );
                mycursor.execute(sql, args)
                mydb.commit()
                handles.append(handle)
    return handles

def insertIntoIntersect(twitters, info):
#new content = [handles], title, date, url
    title = info[0]
    story_number = findIdFromName("Stories", title)
    for handle in twitters:
        handle_number = findIdFromName("Handles", handle)
        sql = "insert ignore into Intersect(story_id, handle_id) values(%s, %s)"
        args = (story_number, handle_number)
        #print('story_id: ' + str(story_number) + '  handle_id: ' + str(handle_number))
        mycursor.execute(sql, args)
        mydb.commit()

def testIfItemExists(table_name, item):
    """Helper function. All the handles and story titles are unqiue. Tells if the story or twitter already exists"""
    if table_name == "Handles":
        column_name = "handle"
    if table_name == "Stories":
        column_name = "title"
    sql = "select {} from {} where {} = %s".format(column_name, table_name, column_name)
    args = (item, )
    mycursor.execute(sql, args)
    data = mycursor.fetchall()
    if not data:
        return False
    else:
        return True


def findIdFromName(table_name, item):
    if table_name == "Handles":
        search_column = "handle"
        column_name = "handle_id"
    if table_name == "Stories":
        search_column = "title"
        column_name = "story_id"
    try:
        sql = "select {} from {} where {} = %s".format(column_name, table_name, search_column)
        args = (item, )
        mycursor.execute(sql, args)
        Id = mycursor.fetchall()
        Id = Id[0]
        Id = Id[0]
        return Id 
    except:
        return -1
        
def closeGap(table_name): 
    """Closing the gap to get rid of the auto incrementing bug."""
    if table_name == "Handles":
        column_name = "handle_id"
    elif  table_name == "Stories":
        column_name = "story_id"
    else:
        return None
    try:
        sql = "select MAX({}) from {}".format(column_name, table_name)
        mycursor.execute(sql)
        number = mycursor.fetchall()
        number = number[0]
        number = number[0]
        number = int(number)
    except:
        number = 0
    finally:
        number += 1
        sql = "ALTER TABLE {} AUTO_INCREMENT={}".format(table_name, number)
        mycursor.execute(sql)
        mydb.commit()


def check_if_bad(handle):
    """This is a helper function. There are specific twitter handles that tend to get pulled that known to be bad, this checks for that."""
    sql = "select EXISTS(select * from bad_handles where handle = %s)"
    args = (handle, )
    mycursor.execute(sql, args)
    bad_handle = mycursor.fetchall()
    bad_handle = bad_handle[0]
    bad_handle = bad_handle[0]
    allowed_characters = re.compile('[a-zA-Z0-9_-]+$')
    if not allowed_characters.match(handle):
        bad_handle = 0
    return bad_handle


