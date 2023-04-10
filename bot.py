"""
Description here.
"""

import sys
print("sys.version: " + sys.version)
print("sys.executable: " + sys.executable)

import os
import telebot

# Create an instance of the Telebot class with the API Token
BOT_TOKEN = os.environ.get('BOT_TOKEN')
bot = telebot.TeleBot(BOT_TOKEN)

# Message handlers - for commands
@bot.message_handler(commands=['start'])
def start_handler(message):
    string = f"hello {message.from_user.first_name.lower()}:)"
    string += "\nplease use the command addexpense to start."
    bot.reply_to(message, string)

@bot.message_handler(commands=['addexpense'])
def expense_start__handler(message):
    string = "sure! how much do you want to add?"
    sent_message = bot.send_message(chat_id=message.chat.id, text=string)
    bot.register_next_step_handler(sent_message, expense_getinput_handler)
def expense_getinput_handler(message):
    string = "you want to add $" + message.text
    string += "? y/n"
    sent_message = bot.send_message(chat_id=message.chat.id, text=string)
    bot.register_next_step_handler(sent_message, expense_final_handler)
def expense_final_handler(message):
    if message.text == "y":
        print("write this to csv")
        string = "ok! i've added it to your expenses."
        bot.send_message(chat_id=message.chat.id,text=string)
    else:
        string = "o ok i'll ignore this request."
        bot.send_message(chat_id=message.chat.id,text=string)


bot.infinity_polling()
