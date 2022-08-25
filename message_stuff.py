def get_user_info(message):
#-----------------------------------------------------------------------------
#                           REMOVING NONE
#-----------------------------------------------------------------------------
    #get full user info (from hello message -> check if admin)  
    user_info = [message.from_user.id, message.from_user.username, message.from_user.first_name, message.from_user.last_name]
    
    #if there is no value, write empty
    while True:
        try:
            #loop until no more 'None' left
            if user_info.index(None):
                user_info[user_info.index(None)] = 'empty'  
        except Exception as e:
            print(e)
            break;
    return user_info
            
   
def get_chat_info(message):
#-----------------------------------------------------------------------------
#                           REMOVING NONE
#-----------------------------------------------------------------------------
    #get chat info 
    chat_info = [message.chat.id, message.chat.title]
    while True:
        try:
        #loop until no more 'None' left
            if chat_info.index(None):
                chat_info[chat_info.index(None)] = 'empty'
        except Exception as e:
            print(e)
            break;
    return chat_info
