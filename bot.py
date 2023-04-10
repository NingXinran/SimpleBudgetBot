"""
Description here.
"""
import os
import telebot
from datetime import datetime
from csv import writer
import pandas as pd
from dotenv import load_dotenv

print("*** running bot.py ***")
expense_instance = []

load_dotenv()

# Create an instance of the Telebot class with the API Token
CHAT_ID = os.environ.get('CHAT_ID')
BOT_TOKEN = os.environ.get('BOT_TOKEN')
bot = telebot.TeleBot(BOT_TOKEN)

def get_total_expenses():
    # open the file as pandas dataframe
    expenses_df = pd.read_csv(f"{datetime.today().month}-{datetime.today().year}_expenses.csv", header=None, index_col=0)
    total = 0
    for i in range(expenses_df.shape[0]):
        total += expenses_df.iloc[i].sum()
    return total

# Message handlers - for commands
@bot.message_handler(commands=['start'])
def start_handler(message):
    string = f"hello {message.from_user.first_name.lower()}:)"
    string += "\n/view -> view all expenses for this month"
    string += "\n/add -> add an expense for the day"
    bot.reply_to(message, string)

@bot.message_handler(commands=['add'])
def meals_handler(message):
    print("starting new expense_instance")
    expense_instance.append(datetime.today().strftime('%d/%m/%Y'))
    print(expense_instance)
    string = "hey xinran! please input your expenditure from today."
    bot.send_message(chat_id=message.chat.id, text=string)
    sent_message = bot.send_message(chat_id=message.chat.id,
                                    text="first, how much did you spend on meals?")
    bot.register_next_step_handler(sent_message, drinks_handler)
def drinks_handler(message):
    expense_instance.append(message.text)
    print(expense_instance)

    string = "ok i'll add $" + message.text + " to meals."
    bot.send_message(chat_id=message.chat.id, text=string)
    sent_message = bot.send_message(chat_id=message.chat.id,
                                    text="second, how much did you spend on drinks?")
    bot.register_next_step_handler(sent_message, others_handler)
def others_handler(message):
    expense_instance.append(message.text)
    print(expense_instance)

    string = "ok i'll add $" + message.text + " to drinks."
    bot.send_message(chat_id=message.chat.id, text=string)
    sent_message = bot.send_message(chat_id=message.chat.id,
                                    text="lastly, how much did you spend on miscellaneous?")
    bot.register_next_step_handler(sent_message, final_handler)
def final_handler(message):
    expense_instance.append(message.text)
    print(expense_instance)
    print()

    string = "ok i'll add $" + message.text + " to miscellaneous."

    with open(f"{datetime.today().month}-{datetime.today().year}_expenses.csv", 'a') as f:
        f_writer = writer(f)
        f_writer.writerow(expense_instance)
        f.close()

    bot.send_message(chat_id=message.chat.id, text=string)
    bot.send_message(chat_id=message.chat.id, 
                     text="you're all set! your current total expenses for this month is: $" + 
                            str(get_total_expenses()))

    print("updated csv")
    expense_instance.clear()
    print("expense_instance cleared.")

@bot.message_handler(commands=['view'])
def view_handler(message):
    # open the file as pandas dataframe
    expenses_df = pd.read_csv(f"{datetime.today().month}-{datetime.today().year}_expenses.csv", header=None, index_col=0)
    total = get_total_expenses() 
    string = "your list of expenses:\n"
    string += "date/meals/drinks/misc\n"
    df_string = expenses_df.to_string()
    df_string = df_string[28:]
    string += df_string
    bot.send_message(chat_id=message.chat.id, text=string) 
    bot.send_message(chat_id=message.chat.id, text="your current total expenses for this month is: $" + str(total))

def daily_reminder():
    bot.send_message(chat_id=CHAT_ID, text="hey xinran, type /add to track your expenses for today:)")

bot.infinity_polling()
