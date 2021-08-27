import telebot
from telebot import types
import config
bot = telebot.TeleBot(config.API_TOKEN)
import datetime
from dateutil.relativedelta import relativedelta
current_date = datetime.datetime.now().date()

year = 0
month = 0
day = 0

user_data = {}

class User:
    def __init__(self, first_name):
        self.first_name = first_name
        self.last_name = ''
        self.age = ''

markup_next = types.ReplyKeyboardMarkup(row_width=1)
itembtn1 = types.KeyboardButton('NEXT')
markup_next.add(itembtn1)

markup = types.ReplyKeyboardMarkup(row_width=2)
itembtn1 = types.KeyboardButton('YES')
itembtn2 = types.KeyboardButton('NO')
markup.add(itembtn1, itembtn2)
hideBoard = types.ReplyKeyboardRemove()

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    if message.text == '/start':
        msg = bot.send_message(message.chat.id, "Do you want to look for cars and to know them costs?", reply_markup=markup)
        bot.register_next_step_handler(msg, process_look_for_step)
    elif message.text == '/help':
        bot.send_message(message.chat.id, "Write '/start'!")

def process_look_for_step(message):
    if message.text == 'YES':
        msg = bot.send_message(message.chat.id, "Ok. Are you registered?", reply_markup=markup)
        bot.register_next_step_handler(msg, process_registration_step)
    elif message.text == 'NO':
        bot.send_message(message.chat.id, "Oh. Ok. Good bye!")

def process_registration_step(message):
    if message.text == 'YES':
        msg = bot.send_message(message.chat.id, "Oh. Ok. I am funny.", reply_markup=markup_next)
        bot.register_next_step_handler(msg, process_enter_step)
    elif message.text == 'NO':
        msg = bot.send_message(message.chat.id, "Ok! Let's start registration!"
                                                "\nWrite your firstname please!",
                                                reply_markup=hideBoard)
        bot.register_next_step_handler(msg, process_firstname_step)

def process_enter_step(message):
    print("QWERTY")
    bot.send_message(message.chat.id, "I am here!)", reply_markup=hideBoard)

def process_firstname_step(message):
    if len(message.text) <= 15:
        user_id = message.from_user.id
        firstname = message.text
        user = User(firstname)
        user_data[user_id] = user
        msg = bot.send_message(message.chat.id, "Write your lastname please!")
        bot.register_next_step_handler(msg, process_lastname_step)
    else:
        msg = bot.send_message(message.chat.id, "Length your firstname must to be not more 15 characters!"
                                                "\nWrite your firstname please!")
        bot.register_next_step_handler(msg, process_firstname_step)

def process_lastname_step(message):
    if len(message.text) <= 15:
        user_id = message.from_user.id
        lastname = message.text
        user = user_data[user_id]
        user.last_name = lastname
        msg = bot.send_message(message.chat.id, "Write your birthday please!\nWrite your birthday year!")
        bot.register_next_step_handler(msg, process_birthday_year_step)
    else:
        msg = bot.send_message(message.chat.id, "Length your lastname must to be not more 15 characters!"
                                                "\nWrite your lastname please!")
        bot.register_next_step_handler(msg, process_lastname_step)

def process_birthday_year_step(message):
    global year
    year = message.text
    try:
        int(year)
        if len(year) == 4 and year.isdigit():
            msg = bot.send_message(message.chat.id, "Write number your birthday month!")
            bot.register_next_step_handler(msg, process_birthday_month_step)
        else:
            msg = bot.send_message(message.chat.id, "You must to write four-digit integer!"
                                                    "\nWrite your birthday year!")
            bot.register_next_step_handler(msg, process_birthday_year_step)
    except Exception:
        msg = bot.send_message(message.chat.id, "You must to write four-digit integer!"
                                                "\nWrite your birthday year!")
        bot.register_next_step_handler(msg, process_birthday_year_step)

def process_birthday_month_step(message):
    global month
    month = message.text
    try:
        int(month)
        if 0 < len(month) < 3 and 0 < int(month) <=12 and month.isdigit():
            msg = bot.send_message(message.chat.id, "Write number your birthday day!")
            bot.register_next_step_handler(msg, process_birthday_day_step)
        else:
            msg = bot.send_message(message.chat.id, "You must to write one-digit or two-digit integer!"
                                                    "\nWrite number your birthday month!")
            bot.register_next_step_handler(msg, process_birthday_month_step)
    except Exception:
        msg = bot.send_message(message.chat.id, "You must to write one-digit or two-digit integer!"
                                                "\nWrite number your birthday month!")
        bot.register_next_step_handler(msg, process_birthday_month_step)

def process_birthday_day_step(message):
    global day
    day = message.text
    try:
        int(day)
        if 0 < len(day) < 3 and 0 < int(month) < 32 and month.isdigit():
            my_date_birthday = datetime.date(int(year), int(month), int(day))
            our_age = relativedelta(current_date, my_date_birthday).years
            user_id = message.from_user.id
            print(user_id)
            user = user_data[user_id]
            age = str(our_age)
            user.age = age
            msg = bot.send_message(message.chat.id, "You have successfully registered!"
                                                    "\nYour first name : " + user.first_name +
                                                    "\nYour last name : " + user.last_name +
                                                    "\nYour age : " + user.age +
                                                    "\nYour birthday : " + my_date_birthday.strftime("%m/%d/%Y") +
                                                    "\nYour date of registration : " + current_date.strftime("%m/%d/%Y"), reply_markup=markup_next)
            bot.register_next_step_handler(msg, process_enter_step)
        else:
            msg = bot.send_message(message.chat.id, "You must to write one-digit or two-digit integer!"
                                                    "\nWrite number your birthday day!")
            bot.register_next_step_handler(msg, process_birthday_day_step)
    except Exception:
        msg = bot.send_message(message.chat.id, "You must to write one-digit or two-digit integer!"
                                                "\nWrite number your birthday day!")
        bot.register_next_step_handler(msg, process_birthday_day_step)

bot.polling()

