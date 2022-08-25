import mysql.connector

def connect():
    try:
        db = mysql.connector.connect(
          host="192.168.254.215",
          user="bot",
          password="Bot0803!999",
          database="tyfla_bot"
        )
        cursor = db.cursor()
        print('connection to database opened correctly')
        #print(db, cursor)
    except Exception as e:
            print('DATABASE ERROR: ', e)
    return [db, cursor]

def close_connection(db, cursor):
    try:
        cursor.close()
        db.close()
        print('connection to database closed correctly')
    except Exception as e:
        print('DATABASE ERROR: ', e)
#-----------------------------------------------------------------------------
#               GET USER FROM GROUP FOR TAGGING
#-----------------------------------------------------------------------------
def get_user_tag_groups(user_info, chat_info, selection):
#nmz einai axrista ta if
    if selection == '/val':
       selection='Valorant'
    elif selection == '/sot':
       selection='Sea of thieves'
    elif selection == '/apex':
       selection='Apex Legends'
       
    sql = 'SELECT G.id, G.user_id, U.tag, G.selection FROM users U  JOIN groups G ON (G.selection ='+str(selection)+') AND (U.user_id=G.user_id) AND (U.group_id=G.group_id) AND G.group_id=' + str(chat_info[0])
    try:
        connection = connect()
        db = connection[0]
        cursor = connection[1]
        cursor.execute(sql)
        res = cursor.fetchall()   #epistrefei list [] apo arrays (), ara prepei na ginei [()]   !!!
        for i in range(0, len(res)):
            print('duo', res[i])
        close_connection(cursor, db)
    except Exception as e:
        print('ERROR: ', e)
        close_connection(cursor, db)
    tags = ''
    for i in range(0, len(res)):
        x = res[i]
        tags += '@'+x[2]+' '
        print(tags)
    return tags

    
#-----------------------------------------------------------------------------
#               ADDING USER TO GROUP FOR TAGGING
#-----------------------------------------------------------------------------
def add_user_to_tag_group(user_id, chat_info, selection):
    #kapoia stigmh na stelnei ola ta options mazemena
    sql_query = "INSERT INTO groups (user_id, group_id, selection) VALUES (%s, %s, %s)"
    print(type(selection), selection)
    num_of_rows_to_add = len(selection)
    #connect to db
    connection = connect()
    db = connection[0]
    cursor = connection[1]
    #set names to selection numbers
    add_me_in=[]
    for i in range(0, num_of_rows_to_add):
        if selection[i] == 0:
            add_me_in.append('Valorant')
        elif selection[i] == 1:
            add_me_in.append('Sea of Thieves')
        elif selection[i] == 2:
            add_me_in.append('Apex Legends')
        elif selection[i] == 3:
            add_me_in.append('Boys Club')
        elif selection[i] == 4:
            add_me_in.append('Girls Club')
    #add each selection to database
    for i in range(0, num_of_rows_to_add):
        try:
            values=(user_id, chat_info[0], add_me_in[i])
            print(values)
            cursor.execute(sql_query, values)
            db.commit()
        except Exception as e:
            print('DATABASE: ', e)
    close_connection(cursor, db)
    #return rasult
    return "You are already in database"
#-----------------------------------------------------------------------------
#               ADDING USER TO DATABASE
#-----------------------------------------------------------------------------
def user_to_db(user_info,chat_info):
    sql_query="INSERT INTO users (user_id, tag, first_name, last_name, group_id) VALUES (%s, %s, %s, %s, %s)"
    values=(user_info[0], user_info[1], user_info[2], user_info[3], chat_info[0])
    try:
        connection = connect()
        db = connection[0]
        cursor = connection[1]
        cursor.execute(sql_query, values)
        db.commit()
        close_connection(cursor, db)
        return "You have been added to database"
    except Exception as e:
        print('DATABASE: ', e)
        close_connection(cursor, db)
        return "You are already in database"
#-----------------------------------------------------------------------------
#               TAG USERS FROM CHAT
#-----------------------------------------------------------------------------
def get_user_tags(user_info, chat_info):
    try:
        connection = connect()
        db = connection[0]
        cursor = connection[1]
        cursor.execute("SELECT tag FROM users WHERE group_id=" + str(chat_info[0]))
        res = cursor.fetchall()   #epistrefei list [] apo arrays (), ara prepei na ginei [()]   !!!
        close_connection(cursor, db)
        tags=''
        for x in res:
            if x[0] == user_info[1]:
                continue
            tags = tags + "@"+x[0] + ' '
        for x in res:
            print(x[0])
    except Exception as e:
        print('DATABASE: ', e)
        close_connection(cursor, db)
        
        
    return tags
#-----------------------------------------------------------------------------
#               AUTHORIZE USER 
#-----------------------------------------------------------------------------
def admin_auth(user_info, chat_info):
    try:
        sql = "SELECT user_id FROM admins WHERE group_id = " + str(chat_info[0])
        connection = connect()
        db = connection[0]
        cursor = connection[1]
        cursor.execute(sql)
        res = cursor.fetchall()
        close_connection(cursor, db)
        for row in res:
            try:
                if row.index(user_info[0]) == 0:
                    print(user_info[0], "is an admin")
                    return 'You are 1 of '+ str(cursor.rowcount) + ' authorized users.'
            except Exception as e:
                print('searching...')
            print('no more admins to check...')     
        return 'You are not authorized.'
    except Exception as e:
        print('DATABASE: ', e)
        close_connection(cursor, db)
        

#-----------------------------------------------------------------------------
#               MAKE USER ADMIN
#-----------------------------------------------------------------------------
def make_admin(user_info, chat_info):
    try:
        sql_query="INSERT INTO admins (user_id, group_id) VALUES (%s, %s)"
        values=(user_info[0], chat_info[0])
        connection = connect()
        db = connection[0]
        cursor = connection[1]
        cursor.execute(sql_query, values)
        db.commit()
        close_connection(cursor, db)
        return "You have been added as an admin"
    except Exception as e:
        print('DATABASE: ', e)
        close_connection(cursor, db)
        return "You are already an admin"
    
