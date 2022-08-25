import telebot
import time
import telegram
import mysql.connector
from telebot import types
from database_stuff import *
from message_stuff import *
from add_user_to_tag_group import *
#from menu import *

chat_info = []
user_info = []
bot_info = []

bot = telebot.TeleBot('5164156205:AAFfNonv0jaoGoRx2wmpi_PlRlN0Mh1VdfI')
bot_info = [bot.get_me().id, bot.get_me().username]

# handling Poll answers
@bot.poll_answer_handler()
def handle_poll_answer(pollAnswer):
    try:
        selection=pollAnswer.option_ids
        user_id=pollAnswer.user.id      
        add_user_to_tag_group(user_id, chat_info, selection)     
    except Exception as e:
        print('POLL: ', e)
    
    

@bot.message_handler(['start', 'hello', 'get_tags', 'add_me', 'make_me_admin', 'info', 'group', 'val', 'sot', 'apex'])
def send_welcome(message):
   # try:
        #user_info = get_user_info(message)
        #chat_info = get_chat_info(message)
        #bot.send_message(chat_info[0], "hello {name}".format(name=user_info[2]))
   
        ##      TESTING START
        if message.text == '/group':
            user_info = get_user_info(message)
            global chat_info #shmantiko to global ekei giati allios den vlepei thn chat_info anathesh
            chat_info = get_chat_info(message)
            select_group_poll(user_info, chat_info, bot)
        if message.text == '/val' or message.text == '/sot' or message.text == '/apex':
            user_info = get_user_info(message)
            chat_info = get_chat_info(message)
            tags = get_user_tag_groups(user_info, chat_info, message.text)
            if len(tags) == 0:
                bot.send_message(chat_info[0], "Haven't captured any tags yet.")
            else:
                bot.send_message(chat_info[0], tags)
        if message.text == '/info':
            user_info = get_user_info(message)
            chat_info = get_chat_info(message)
            reply = ["/hello", '/get_tags', '/add_me', '/make_me_admin']
            reply_all=""
            for i in reply:
                reply_all=reply_all+'\n'+i
            bot.send_message(chat_info[0], reply_all)
        if message.text == '/hello':
            #ekkinisi twn admin commands
            user_info = get_user_info(message)
            chat_info = get_chat_info(message)
            reply = admin_auth(user_info, chat_info)
            #go to private chat if user is admin
            if reply != 'You are not authorized.':
                bot.send_message(chat_info[0], 'Check your inbox 📥\n'+reply)
                group_chat = chat_info[0]
                bot.send_message(user_info[0], 'hello '+user_info[2])

        if message.text == '/make_me_admin':
            #make a user an admin (thelei diorthosi, prepei na dinei poion xristi thelei gia admin)
            user_info = get_user_info(message)
            chat_info = get_chat_info(message)
            reply = make_admin(user_info, chat_info)
            bot.send_message(chat_info[0], reply)
        
        if message.text == '/add_me':
            #testing database adding user
            user_info = get_user_info(message)
            chat_info = get_chat_info(message)
            reply = user_to_db(user_info,chat_info)
            bot.send_message(chat_info[0], reply)
        
        if message.text == '/get_tags':
            #tag @all
            user_info = get_user_info(message)
            chat_info = get_chat_info(message)
            tags=get_user_tags(user_info, chat_info)
            if len(tags) == 0:
                bot.send_message(chat_info[0], "Haven't captured any tags yet.")
            else:
                bot.send_message(chat_info[0], tags)          
        ##      TESTING END
    #except Exception as e:
       # print('test',e)
            
#Που ακούει όλα τα μηνύματα
#def listener(chat):
#    for message in chat:        
#        print('ok')
#bot.set_update_listener(listener)

#Αναγκαστικό για να ξεκιήσει το Bot
try:
    bot.infinity_polling(timeout=10, long_polling_timeout = 5)
    print('\nCONNECTING AGAIN\n')
except Exception as e:
    print(e)

