import time
import telegram
from database_stuff import *

options=('Valorant', 'Sea of Thieves', 'Apex Legends', 'Boys Club', 'Girls Club')

def select_group_poll(user_info, chat_info, bot):
    
    try:
        #connect to db
        connection = connect()
        db = connection[0]
        cursor = connection[1]
        
        #get user partisipation in groups
        sql = 'SELECT  G.selection FROM users U  JOIN groups G ON (U.user_id=G.user_id) AND (U.group_id=G.group_id) AND G.group_id=' + str(chat_info[0])
        cursor.execute(sql)
        res = cursor.fetchall()
        
        #make the poll options based on the groups tha the user is in
        user_defined_options = list(options)
        groups_is_in_list = []
        
        #get group names in a list
        for is_in_group in res:
            for i in range(len(is_in_group)):
                groups_is_in_list.append(is_in_group[i])
        print('User is in: ',groups_is_in_list)

        print('Original list is: ', user_defined_options)
        
        #make new list and exclude groups from above list
        for already_in in groups_is_in_list:
            for option in options:
                if option == already_in:
                    #delete option from the list
                    user_defined_options[user_defined_options.index(option)]= option +  "\t| already in | " 
                    print('tweaking', option)
        print('New list is: ', user_defined_options)
        
        #send the now new list               
        res = bot.send_poll(chat_id=chat_info[0], question='Διέλεξε τα παιχνίδια που παίζεις:', options=user_defined_options, open_period=10, type='regular', allows_multiple_answers=True, is_anonymous=False)  
    except Exception as e:
        print(e)
