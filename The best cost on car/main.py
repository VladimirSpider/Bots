import telebot
from telebot import types
import config
bot = telebot.TeleBot(config.API_TOKEN)
import datetime
from dateutil.relativedelta import relativedelta
import mysql.connector

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="root",
  port = "3306",
  database = "The_best_cost_on_car"
)
print(mydb)
#Создание базы данных
mycursor = mydb.cursor()

#(1-step)
#mycursor.execute("CREATE DATABASE The_best_cost_on_car")

#(2-step)
'''
mycursor.execute("CREATE TABLE Users (id INT AUTO_INCREMENT PRIMARY KEY,\
                 user_id INT,\
                 first_name VARCHAR(255),\
                 last_name VARCHAR(255),\
                 age INT,\
                 birthday VARCHAR(255),\
                 date_of_registration VARCHAR(255),\
                 password VARCHAR(255))")
'''

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
        self.password = ''
        self.birthday = ''

markup_enter = types.ReplyKeyboardMarkup(row_width=1)
itembtn1 = types.KeyboardButton('ENTER')
markup_enter.add(itembtn1)

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
    else:
        msg = bot.send_message(message.chat.id, "Press one of these keys please!"
                                                "\nDo you want to look for cars and to know them costs?",
                                                reply_markup=markup)
        bot.register_next_step_handler(msg, process_look_for_step)

def process_registration_step(message):
    if message.text == 'YES':
        msg = bot.send_message(message.chat.id, "You must enter in your account!", reply_markup=markup_enter)
        bot.register_next_step_handler(msg, process_enter_step1)
    elif message.text == 'NO':
        msg = bot.send_message(message.chat.id, "Ok! Let's start registration!"
                                                "\nWrite your firstname please!",
                                                reply_markup=hideBoard)
        bot.register_next_step_handler(msg, process_firstname_step)
    else:
        msg = bot.send_message(message.chat.id, "Press one of these keys please!"
                                                "\nOk. Are you registered?",
                                                reply_markup=markup)
        bot.register_next_step_handler(msg, process_registration_step)

def process_enter_step1(message):
    if message.text == 'ENTER':
        msg = bot.send_message(message.chat.id, "Write your firstname!", reply_markup=hideBoard)
        bot.register_next_step_handler(msg, process_enter_step2)
    else:
        msg = bot.send_message(message.chat.id, "Press this keys please!"
                                                "\nYou must enter in your account!",
                                                reply_markup=markup_enter)
        bot.register_next_step_handler(msg, process_enter_step1)

def process_enter_step2(message):
    user_id = message.from_user.id
    firstname = message.text
    user = User(firstname)
    user_data[user_id] = user
    msg = bot.send_message(message.chat.id, "Write your password please!")
    bot.register_next_step_handler(msg, process_enter_step)

def process_enter_step(message):
    test_list = []
    user_id = message.from_user.id
    password = message.text
    user = user_data[user_id]
    user.password = password
    sql = "SELECT first_name, password FROM Users WHERE user_id = " + str(user_id)
    mycursor.execute(sql)
    myresult = mycursor.fetchall()
    print(myresult)
    if len(myresult) == 0:
        msg = bot.send_message(message.chat.id, "You are not registered!"
                                                "\nYou must registered!"
                                                "\nDo you try it?", reply_markup = markup)
        user_data.clear()
        bot.register_next_step_handler(msg, process_look_for_step)
    elif len(myresult) != 0:
        for x in myresult:
            if user.first_name in x and user.password in x:
                test_list.append(1)
        if len(test_list) > 0:
            bot.send_message(message.chat.id, "You are enter!"
                                              "\nYour first name : " + user.first_name +
                                              "\nYour password : " + user.password)
            test_list.clear()
            user_data.clear()
        else:
            msg = bot.send_message(message.chat.id, "Your data are not correct!"
                                                    "\nYour first name : " + user.first_name +
                                                    "\nYour password : " + user.password +
                                                    "\nTry again!", reply_markup=markup)
            test_list.clear()
            user_data.clear()
            bot.register_next_step_handler(msg, process_look_for_step)



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
            user.birthday = my_date_birthday.strftime("%m/%d/%Y")
            print(user.birthday)
            print(type(user.birthday))
            msg = bot.send_message(message.chat.id, "Write your password!"
                                                    "\nMinimum length your password 5 characters,"
                                                    "\nmaximum length your password 10 characters!")
            bot.register_next_step_handler(msg, process_password_step)
        else:
            msg = bot.send_message(message.chat.id, "You must to write one-digit or two-digit integer!"
                                                    "\nWrite number your birthday day!")
            bot.register_next_step_handler(msg, process_birthday_day_step)
    except Exception:
        msg = bot.send_message(message.chat.id, "You must to write one-digit or two-digit integer!"
                                                "\nWrite number your birthday day!")
        bot.register_next_step_handler(msg, process_birthday_day_step)

def process_password_step(message):
    if 5 <= len(message.text) <= 10:
        user_id = message.from_user.id
        password = message.text
        user = user_data[user_id]
        user.password = password
        sql = "INSERT INTO Users (user_id, first_name, last_name, age, birthday, date_of_registration, password) VALUES (%s, %s, %s, %s, %s, %s, %s)"
        val = (user_id, user.first_name, user.last_name, user.age, user.birthday, current_date.strftime("%m/%d/%Y"),
               user.password)
        mycursor.execute(sql, val)
        mydb.commit()
        msg = bot.send_message(message.chat.id, "You have successfully registered!"
                                                "\nYou must enter in your account!"
                                                "\nYour first name : " + user.first_name +
                                                "\nYour last name : " + user.last_name +
                                                "\nYour age : " + user.age +
                                                "\nYour password : " + user.password +
                                                "\nYour birthday : " + user.birthday +
                                                "\nYour date of registration : " + current_date.strftime("%m/%d/%Y"), reply_markup=markup_enter)
        user_data.clear()
        bot.register_next_step_handler(msg, process_enter_step1)
    else:
        msg = bot.send_message(message.chat.id, "Write your password!"
                                                "\nMinimum length your password 5 characters,"
                                                "\nmaximum length your password 10 characters!")
        bot.register_next_step_handler(msg, process_password_step)

bot.polling()

