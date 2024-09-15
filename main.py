import pyautogui as pg
import pyperclip as pp
import telebot as tb
from telebot import types
import json, time


try:
    w = pg.getWindowsWithTitle("Backyard AI")[0]
    w.activate()
except:
     print("Backyard is not launched")

user_message=None
chat_generation_time = 5 #seconds

def get_location(image):
    try:
        return pg.center(pg.locateOnScreen(image, grayscale=True, confidence=.9))
    except:
         print("multiple requests to bot error")

def save_json_chat():
     pg.click(get_location('downward_arrow.png'))
     pg.click(get_location('export_chat.png'))
     time.sleep(0.3)
     pg.doubleClick()
     pg.click(get_location('json.png'))
     pg.press('enter')
     time.sleep(0.2)
     pg.press('left')
     pg.press('enter')
     time.sleep(0.2)
     w.activate()
    
def write_a_message(user_message):
    pg.click(get_location('TypeMessage.png'))
    pp.copy(str(user_message.text))
    pg.hotkey('ctrl', 'v')
    pp.copy('')
    pg.press('enter')
    render_message=bot.send_message(user_message.chat.id,"Please wait for "+str(
        chat_generation_time)+" seconds, generating responce").message_id
    time.sleep(chat_generation_time)
    pg.click(get_location('TypeMessage.png'))
    save_json_chat()
    bot.delete_message(user_message.chat.id, render_message)
    
bot=tb.TeleBot('7431833180:AAE6aE2xg9EMbyLMFUhPRX3huO9k_-_PLS0') #enter token here

#Start 

@bot.message_handler(commands=['start']) #START command
def start(message):
     bot.send_message(message.chat.id,"Hey, I am working on the first message from the bot rn. \nYou can start messaging bot now. \nUse /help to set render time (5 by default) and pre-load bot")

@bot.message_handler(commands=['set_render_time'])
def start(message):
     bot.send_message(message.chat.id,"Type in the new render time:")
     bot.register_next_step_handler(message,set_render_time)

def set_render_time(message):
    if int(message.text)>0:
        global chat_generation_time 
        chat_generation_time = int(message.text)
        bot.send_message(message.chat.id,"The render time is set to "+str(chat_generation_time)+" seconds")
    else:
        bot.send_message(message.chat.id,"Invalid render time")
          
@bot.message_handler(commands=['help']) #HELP
def start(message): 
     bot.send_message(message.chat.id,"You can:\n/load_bot\n/set_render_time")   


@bot.message_handler(commands=['load_bot']) #load bot into memorry
def load_bot(message):
     render_message=bot.send_message(message.chat.id,"Please wait for "+str((chat_generation_time*5))+" seconds, loading bot into memory.").message_id
     pg.click(get_location('TypeMessage.png'))
     pg.typewrite('hi')
     pg.press('Enter')
     time.sleep(chat_generation_time*5)
     pg.click(get_location('Undo.png'))
     pg.press('Backspace')
     pg.press('Backspace')
     bot.delete_message(message.chat.id, render_message)
     bot.send_message(message.chat.id,"Completed!")



#Continue button
@bot.callback_query_handler(func=lambda call:True) #commands continue
def next(message):
     pg.click(get_location('continue.png'))
     time.sleep(chat_generation_time*0.5)
     pg.click(get_location('TypeMessage.png'))
     save_json_chat()
     with open("1.json","r", encoding='utf-8') as f: #oppening json and printing out the last bot's responce
          data = json.load(f)
     markup=types.InlineKeyboardMarkup(row_width=1)
     continue_button=types.InlineKeyboardButton('Continue', callback_data='/continue')
     markup.add(continue_button)
     try:
          bot.edit_message_text(chat_id=current_message_from_bot.chat.id, text=str(data['chat']['ChatItems'][-1]['output']), message_id=current_message_from_bot.message_id,reply_markup=markup)
     except:
          bot.send_message(chat_id=current_message_from_bot.chat.id,text="Empty responce from the model")
     f.close

    


#Any message
@bot.message_handler()
def chat(message):
    markup=types.InlineKeyboardMarkup(row_width=1)
    continue_button=types.InlineKeyboardButton('Continue', callback_data='/continue')
    markup.add(continue_button)
    w.activate()
    write_a_message(message)
    with open("1.json","r", encoding='utf-8') as f: #oppening json and printing out the last bot's responce
            data = json.load(f)

    global current_message_from_bot 
    current_message_from_bot = bot.send_message(message.chat.id,data['chat']['ChatItems'][-1]['output'],reply_markup=markup)
    f.close

bot.polling(none_stop=True)

