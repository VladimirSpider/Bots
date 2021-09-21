import telebot
from telebot import types
import config, dictionaries
from parserAV import parse
bot = telebot.TeleBot(config.API_TOKEN)
import datetime, time
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
#(3-step)
'''mycursor.execute("CREATE TABLE Cars_from_belarus (id INT AUTO_INCREMENT PRIMARY KEY,\
                 car_brand VARCHAR(255),\
                 technical_number INT)")'''

'''for key in sorted(dictionaries.all_cars.keys()):
    print (key, dictionaries.all_cars[key])
    sql = "INSERT INTO Cars_from_belarus (car_brand, technical_number) VALUES (%s, %s)"
    val = (key, dictionaries.all_cars[key])
    mycursor.execute(sql, val)
    mydb.commit()'''

#(4-step)
'''mycursor.execute("CREATE TABLE Model_from_belarus (id INT AUTO_INCREMENT PRIMARY KEY,\
                 id_fk INT,\
                 car_brand VARCHAR(255),\
                 model VARCHAR(255),\
                 technical_number INT,\
                 FOREIGN KEY (id_fk) REFERENCES Cars_from_belarus (id))")'''

#Audi, BMW, Mercedes_Benz, Opel, Volkswagen
'''for key in sorted(dictionaries.Volkswagen.keys()):
    print (key, dictionaries.Volkswagen[key])
    sql = "INSERT INTO Model_from_belarus (id_fk, car_brand, model, technical_number) VALUES (%s, %s, %s, %s)"
    val = (78, "Volkswagen", key, dictionaries.Volkswagen[key])
    mycursor.execute(sql, val)
    mydb.commit()'''

#(5-step)
'''mycursor.execute("CREATE TABLE All_сars (id INT AUTO_INCREMENT PRIMARY KEY,\
                 country VARCHAR(255),\
                 city VARCHAR(255),\
                 title VARCHAR(255),\
                 description VARCHAR(255),\
                 year INT,\
                 cost INT,\
                 link VARCHAR(255))")'''

current_date = datetime.datetime.now().date()

cost_min = ""
cost_max = ""
year_min = ""
year_max = ""

count_listings = 0

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

your_choice = {
    "Brand": "",
    "Model": ""
}
what_model_do_you_want = 0
what_car_do_you_want = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
list_cars = []
list_models = []
for el in dictionaries.cars.keys():
    list_cars.append(el)
itembtn1 = types.KeyboardButton(list_cars[0])
itembtn2 = types.KeyboardButton(list_cars[1])
itembtn3 = types.KeyboardButton(list_cars[2])
itembtn4 = types.KeyboardButton(list_cars[3])
itembtn5 = types.KeyboardButton(list_cars[4])
itembtn6 = types.KeyboardButton("-----")
what_car_do_you_want.add(itembtn1, itembtn2, itembtn3, itembtn4, itembtn5,itembtn6 , "EXIT")

markup_enter = types.ReplyKeyboardMarkup(resize_keyboard= True ,row_width=1)
itembtn1 = types.KeyboardButton('ENTER')
markup_enter.add(itembtn1)

markup = types.ReplyKeyboardMarkup(resize_keyboard= True ,row_width=2)
itembtn1 = types.KeyboardButton('YES')
itembtn2 = types.KeyboardButton('NO')
markup.add(itembtn1, itembtn2)

markup_watch_filter = types.ReplyKeyboardMarkup(resize_keyboard= True ,row_width=2)
itembtn1 = types.KeyboardButton("FILTER")
itembtn2 = types.KeyboardButton("WATCH")
itembtn3 = types.KeyboardButton("BACK")
itembtn4 = types.KeyboardButton("EXIT")
markup_watch_filter.add(itembtn1, itembtn2, itembtn3, itembtn4)

markup_filter_back_exit = types.ReplyKeyboardMarkup(resize_keyboard= True ,row_width=2)
markup_filter_back_exit.row("FILTER")
itembtn1 = types.KeyboardButton("BACK")
itembtn2 = types.KeyboardButton("EXIT")
markup_filter_back_exit.add(itembtn1, itembtn2)

markup_filter = types.ReplyKeyboardMarkup(resize_keyboard= True ,row_width=2)
itembtn1 = types.KeyboardButton("COST: from... to...")
itembtn2 = types.KeyboardButton("YEAR: from... to...")
itembtn3 = types.KeyboardButton("BACK")
itembtn4 = types.KeyboardButton("EXIT")
markup_filter.add(itembtn1, itembtn2, itembtn3, itembtn4)

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
        bot.send_message(message.chat.id, "Oh. Ok. Good bye!"
                                          "\nIf you want start again write '/start'!",  reply_markup=hideBoard)
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
            msg = bot.send_message(message.chat.id, "Ok! You can look for cars in Belarus."
                                                    "\nChose car's brand please.", reply_markup=what_car_do_you_want)
            bot.register_next_step_handler(msg, look_for_car_brand_step)
        else:
            msg = bot.send_message(message.chat.id, "Your data are not correct!"
                                                    "\nYour first name : " + user.first_name +
                                                    "\nYour password : " + user.password +
                                                    "\nDo you try again?", reply_markup=markup)
            test_list.clear()
            user_data.clear()
            bot.register_next_step_handler(msg, process_look_for_step)

def look_for_car_brand_step(message):
    global what_model_do_you_want
    if message.text in list_cars and message.text != "EXIT" and message.text != "-----":
        what_model_do_you_want = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=4)
        global list_models
        for el in dictionaries.cars[message.text].keys():
            list_models.append(el)
        technical_variable = 0
        for i in range(0, len(list_models) + 1):
            if (i % 4 == 0) and (i != 0) and (i != len(list_models)):
                what_model_do_you_want.row(list_models[i - 4], list_models[i - 3], list_models[i - 2], list_models[i - 1])
                technical_variable = i
            if (i == (len(list_models) - 1)):
                technical_number = (i + 1) - (technical_variable)
                if technical_number == 1:
                    what_model_do_you_want.row(list_models[i], "-----", "-----", "-----")
                elif technical_number == 2:
                    what_model_do_you_want.row(list_models[i - 1], list_models[i], "-----", "-----")
                elif technical_number == 3:
                    what_model_do_you_want.row(list_models[i - 2], list_models[i - 1], list_models[i], "-----")
                elif technical_number == 4:
                    what_model_do_you_want.row(list_models[i - 3], list_models[i - 2], list_models[i - 1],
                                               list_models[i])
            elif i == len(list_models):
                what_model_do_you_want.row("EXIT", "BACK")
        your_choice["Brand"] = message.text
        msg = bot.send_message(message.chat.id, f"You chose car - {message.text}! Ok!"
                                                f"\nChose your brand's model please.", reply_markup=what_model_do_you_want)
        bot.register_next_step_handler(msg, look_for_car_model_step)
    elif message.text == "EXIT":
        bot.send_message(message.chat.id, "Oh. Ok. Good bye!"
                                          "\nIf you want start again write '/start'!", reply_markup=hideBoard)
    else:
        msg = bot.send_message(message.chat.id, "Press one of these keys please!"
                                                "\nOk. Chose car's brand please.",
                                                reply_markup=what_car_do_you_want)
        bot.register_next_step_handler(msg, look_for_car_brand_step)

def look_for_car_model_step(message):
    global what_model_do_you_want
    global list_models
    if (message.text in list_models) and message.text != "EXIT" and message.text != "BACK" and message.text != "-----":
        bot.send_message(message.chat.id, f"Wait please! Data is loading.", reply_markup=hideBoard)
        your_choice["Model"] = message.text
        sql = "SELECT technical_number FROM Cars_from_belarus " \
        "where car_brand = %s"
        car_brand = (your_choice["Brand"],)
        mycursor.execute(sql, car_brand)
        myresult_brand = mycursor.fetchall()
        print(myresult_brand)

        sql = "SELECT technical_number FROM Model_from_belarus " \
              "where model = %s"
        car_model = (your_choice["Model"],)
        mycursor.execute(sql, car_model)
        myresult_model = mycursor.fetchall()
        print(myresult_model)
        nc = ""
        nm = ""
        for x in myresult_brand:
            nc = str(x[0])
        for x in myresult_model:
            nm = str(x[0])
        all_cars = parse(nc, nm)
        for key in all_cars.keys():
            sql = "INSERT INTO All_сars (country, city, title, description, year, cost, link) VALUES (%s, %s, %s, %s, %s, %s, %s)"
            val = (all_cars[key]["country"], all_cars[key]["city"], all_cars[key]["title"], all_cars[key]["description"], all_cars[key]["year"], int(all_cars[key]["cost"]), all_cars[key]["link"])
            mycursor.execute(sql, val)
            mydb.commit()
        sql = "SELECT COUNT(*) FROM all_сars"
        mycursor.execute(sql)
        myresult = mycursor.fetchall()
        print(myresult)

        sql = "SELECT country, city, title, description, year, cost, link   FROM All_сars\
              WHERE cost = (SELECT MIN(cost) FROM All_сars)"
        mycursor.execute(sql)
        myresult_min = mycursor.fetchone()
        print(myresult_min)

        sql = "SELECT country, city, title, description, year, cost, link   FROM All_сars\
                      WHERE cost = (SELECT MAX(cost) FROM All_сars)"
        mycursor.execute(sql)
        myresult_max = mycursor.fetchone()
        print(myresult_max)
        bot.send_message(message.chat.id, f"Your choice:"
                                          f"\n{your_choice['Brand']}"
                                          f"\n{your_choice['Model']}"
                                          f"\nOk! Total listings {myresult[0][0]}.")
        bot.send_message(message.chat.id, f"\nMIN. cost:\n{myresult_min[0]} \n{myresult_min[1]} \n{myresult_min[2]} \n{myresult_min[3]} \n{myresult_min[4]} г. \n{myresult_min[5]} $ \n{myresult_min[6]}")
        bot.send_message(message.chat.id, f"\nMAX. cost:\n{myresult_max[0]} \n{myresult_max[1]} \n{myresult_max[2]} \n{myresult_max[3]} \n{myresult_max[4]} г. \n{myresult_max[5]} $ \n{myresult_max[6]}")
        msg = bot.send_message(message.chat.id, f"You can to see all listings"
                                          f"\nin blocks of 5 items."
                                          f"\nAlso you can use filter."
                                          f"\nCOST: from... to..."
                                          f"\nYEAR: from... to..."
                                          , reply_markup=markup_watch_filter)
        bot.register_next_step_handler(msg, user_look_for_car_step)

    elif message.text == "BACK":
        msg = bot.send_message(message.chat.id, "Ok! You can look for cars in Belarus."
                                                "\nChose car's brand please.", reply_markup=what_car_do_you_want)
        bot.register_next_step_handler(msg, look_for_car_brand_step)
        list_models.clear()
        sql = "DELETE FROM All_сars"
        mycursor.execute(sql)
        mydb.commit()
    elif message.text == "EXIT":
        bot.send_message(message.chat.id, "Oh. Ok. Good bye!"
                                          "\nIf you want start again write '/start'!", reply_markup=hideBoard)
        list_models.clear()
        sql = "DELETE FROM All_сars"
        mycursor.execute(sql)
        mydb.commit()
    else:
        print("HI")
        msg = bot.send_message(message.chat.id, "Press one of these keys please!"
                                                "\nOk. Chose your brand's model please.",
                                                reply_markup=what_model_do_you_want)
        bot.register_next_step_handler(msg, look_for_car_model_step)

def user_look_for_car_step(message):
    our_step = 0
    global what_model_do_you_want
    global list_models
    global count_listings
    if message.text == "FILTER":
        msg = bot.send_message(message.chat.id, f"Ok! Will chose cost from... to..."
                                                f"\nor  year from... to...",
                                                reply_markup=markup_filter)
        bot.register_next_step_handler(msg, user_look_for_car_filter_step)
        print("FILTER")
    elif message.text == "WATCH":
        print("WATCH")
        sql = "SELECT * FROM All_сars"
        mycursor.execute(sql)
        myresult = mycursor.fetchall()
        for el in myresult:
            if myresult[count_listings] == el:
                if ((myresult.index(el) + 1) % 5) == 0 and (myresult.index(el) != len(myresult) - 1):
                    our_step = 1
                    bot.send_message(message.chat.id, f"№{count_listings + 1}\n{el[1]} \n{el[2]} \n{el[3]} \n{el[4]} \n{el[5]} г. \n{el[6]} $ \n{el[7]}")
                    count_listings += 1
                    break
                elif myresult.index(el) == len(myresult) - 1:
                    our_step = 2
                    bot.send_message(message.chat.id, f"№{count_listings + 1}\n{el[1]} \n{el[2]} \n{el[3]} \n{el[4]} \n{el[5]} г. \n{el[6]} $ \n{el[7]}")
                    print(count_listings)
                    count_listings = 0
                    break
                else:
                    bot.send_message(message.chat.id, f"№{count_listings+1}\n{el[1]} \n{el[2]} \n{el[3]} \n{el[4]} \n{el[5]} г. \n{el[6]} $ \n{el[7]}")
                count_listings += 1
        if our_step == 1:
            msg = bot.send_message(message.chat.id, f"Press 'WATCH' if you want to see"
                                                    f"\nnext 5 listings!", reply_markup=markup_watch_filter)
            bot.register_next_step_handler(msg, user_look_for_car_step)
        if our_step == 2:
            print(count_listings)
            msg = bot.send_message(message.chat.id, f"Ok! You watched all listings.",
                                                    reply_markup=markup_filter_back_exit)
            bot.register_next_step_handler(msg, user_look_for_car_step)
    elif message.text == "BACK":
        msg = bot.send_message(message.chat.id, f"You chose car - {your_choice['Brand']}! Ok!"
                                                f"\nChose your brand's model please.", reply_markup=what_model_do_you_want)
        sql = "DELETE FROM All_сars"
        mycursor.execute(sql)
        mydb.commit()
        bot.register_next_step_handler(msg, look_for_car_model_step)
    elif message.text == "EXIT":
        bot.send_message(message.chat.id, "Oh. Ok. Good bye!"
                                          "\nIf you want start again write '/start'!", reply_markup=hideBoard)
        list_models.clear()
        sql = "DELETE FROM All_сars"
        mycursor.execute(sql)
        mydb.commit()
    else:
        print("HI")
        msg = bot.send_message(message.chat.id, "Press one of these keys please!"
                                                "\nOk. Chose your brand's model please.",
                                                reply_markup=markup_watch_filter)
        bot.register_next_step_handler(msg, user_look_for_car_step)

def user_look_for_car_filter_step(message):
    if message.text == "COST: from... to...":
        msg = bot.send_message(message.chat.id, "Cost must to be more or equal 0 $"
                                                "\nand cost must to be less or equal 1000000 $."
                                                "\nMinimal cost must to be less or equal maximal cost!"
                                                "\nOk! Write minimal cost.",
                                                reply_markup=hideBoard)
        bot.register_next_step_handler(msg, user_look_for_car_filter_min_cost_step)
    elif message.text == "YEAR: from... to...":
        msg = bot.send_message(message.chat.id, "Year must to be more or equal 1950"
                                                "\nand year must to be less or equal 2021."
                                                "\nMinimal year must to be less or equal maximal year!"
                                                "\nOk! Write minimal year.",
                                                reply_markup=hideBoard)
        bot.register_next_step_handler(msg, user_look_for_car_filter_min_year_step)
    elif message.text == "BACK":
        bot.send_message(message.chat.id, f"Wait please! Data is loading.", reply_markup=hideBoard)
        global what_model_do_you_want
        global list_models
        sql = "SELECT COUNT(*) FROM all_сars"
        mycursor.execute(sql)
        myresult = mycursor.fetchall()
        print(myresult)

        sql = "SELECT country, city, title, description, year, cost, link   FROM All_сars\
                      WHERE cost = (SELECT MIN(cost) FROM All_сars)"
        mycursor.execute(sql)
        myresult_min = mycursor.fetchone()
        print(myresult_min)

        sql = "SELECT country, city, title, description, year, cost, link   FROM All_сars\
                              WHERE cost = (SELECT MAX(cost) FROM All_сars)"
        mycursor.execute(sql)
        myresult_max = mycursor.fetchone()
        print(myresult_max)
        bot.send_message(message.chat.id, f"Your choice:"
                                          f"\n{your_choice['Brand']}"
                                          f"\n{your_choice['Model']}"
                                          f"\nOk! Total listings {myresult[0][0]}.")
        bot.send_message(message.chat.id,
                         f"\nMIN. cost:\n{myresult_min[0]} \n{myresult_min[1]} \n{myresult_min[2]} \n{myresult_min[3]} \n{myresult_min[4]} г. \n{myresult_min[5]} $ \n{myresult_min[6]}")
        bot.send_message(message.chat.id,
                         f"\nMAX. cost:\n{myresult_max[0]} \n{myresult_max[1]} \n{myresult_max[2]} \n{myresult_max[3]} \n{myresult_max[4]} г. \n{myresult_max[5]} $ \n{myresult_max[6]}")
        msg = bot.send_message(message.chat.id, f"You can to see all listings"
                                                f"\nin blocks of 5 items."
                                                f"\nAlso you can use filter."
                                                f"\nCOST: from... to..."
                                                f"\nYEAR: from... to..."
                               , reply_markup=markup_watch_filter)
        bot.register_next_step_handler(msg, user_look_for_car_step)
    elif message.text == "EXIT":
        bot.send_message(message.chat.id, "Oh. Ok. Good bye!"
                                          "\nIf you want start again write '/start'!", reply_markup=hideBoard)
        list_models.clear()
        sql = "DELETE FROM All_сars"
        mycursor.execute(sql)
        mydb.commit()

def user_look_for_car_filter_min_cost_step(message):
    global cost_min
    cost_min = message.text
    try:
        int(cost_min)
        if len(cost_min) <= 7 and int(cost_min) <= 999999 and cost_min.isdigit():
            msg = bot.send_message(message.chat.id, "Ok! Write maximal cost.")
            bot.register_next_step_handler(msg, user_look_for_car_filter_max_cost_step)
        else:
            msg = bot.send_message(message.chat.id, "You must to write integer!"
                                                    "\nCost must to be more or equal 0 $"
                                                    "\nand cost must to be less or equal 1000000 $."
                                                    "\nMinimal cost must to be less or equal maximal cost!"
                                                    "\nOk! Write minimal cost.")
            bot.register_next_step_handler(msg, user_look_for_car_filter_min_cost_step)
    except Exception:
        msg = bot.send_message(message.chat.id, "You must to write integer!"
                                                "\nCost must to be more or equal 0 $"
                                                "\nand cost must to be less or equal 1000000 $."
                                                "\nMinimal cost must to be less or equal maximal cost!"
                                                "\nOk! Write minimal cost.")
        bot.register_next_step_handler(msg, user_look_for_car_filter_min_cost_step)

def user_look_for_car_filter_max_cost_step(message):
    global cost_min
    global cost_max
    cost_max = message.text
    try:
        int(cost_max)
        if len(cost_max) <= 7 and int(cost_max) <= 1000000 and cost_max.isdigit() and (int(cost_max) >= int(cost_min)):
            bot.send_message(message.chat.id, f"Ok! \nYour filter:\ncost min: {cost_min}\ncost max: {cost_max}")
            bot.send_message(message.chat.id, f"Wait please! Data is loading.", reply_markup=hideBoard)
            global what_model_do_you_want
            global list_models

            sql = "SELECT COUNT(*) FROM all_сars " \
                  "WHERE cost >= %s and cost <= %s"
            cost = (cost_min, cost_max,)
            mycursor.execute(sql, cost)
            myresult = mycursor.fetchall()
            print(myresult)

            sql = "SELECT country, city, title, description, year, cost, link   FROM All_сars\
                                  WHERE cost = (SELECT MIN(cost) FROM All_сars)"
            mycursor.execute(sql)
            myresult_min = mycursor.fetchone()
            print(myresult_min)

            sql = "SELECT country, city, title, description, year, cost, link   FROM All_сars\
                                          WHERE cost = (SELECT MAX(cost) FROM All_сars)"
            mycursor.execute(sql)
            myresult_max = mycursor.fetchone()
            print(myresult_max)
            bot.send_message(message.chat.id, f"Your choice:"
                                              f"\n{your_choice['Brand']}"
                                              f"\n{your_choice['Model']}"
                                              f"\nOk! Total listings {myresult[0][0]}.")
            bot.send_message(message.chat.id,
                             f"\nMIN. cost:\n{myresult_min[0]} \n{myresult_min[1]} \n{myresult_min[2]} \n{myresult_min[3]} \n{myresult_min[4]} г. \n{myresult_min[5]} $ \n{myresult_min[6]}")
            bot.send_message(message.chat.id,
                             f"\nMAX. cost:\n{myresult_max[0]} \n{myresult_max[1]} \n{myresult_max[2]} \n{myresult_max[3]} \n{myresult_max[4]} г. \n{myresult_max[5]} $ \n{myresult_max[6]}")
            msg = bot.send_message(message.chat.id, f"You can to see all listings"
                                                    f"\nin blocks of 5 items."
                                                    f"\nAlso you can use filter."
                                                    f"\nCOST: from... to..."
                                                    f"\nYEAR: from... to..."
                                                    , reply_markup=markup_watch_filter)
            bot.register_next_step_handler(msg, user_look_for_car_step)
        else:
            msg = bot.send_message(message.chat.id, "You must to write integer!"
                                                    "\nCost must to be more or equal 0 $"
                                                    "\nand cost must to be less or equal 1000000 $."
                                                    "\nMinimal cost must to be less or equal maximal cost!"
                                                    "\nOk! Write maximal cost.")
            bot.register_next_step_handler(msg, user_look_for_car_filter_max_cost_step)
    except Exception:
        msg = bot.send_message(message.chat.id, "You must to write integer!"
                                                "\nCost must to be more or equal 0 $"
                                                "\nand cost must to be less or equal 1000000 $."
                                                "\nMinimal cost must to be less or equal maximal cost!"
                                                "\nOk! Write maximal cost.")
        bot.register_next_step_handler(msg, user_look_for_car_filter_max_cost_step)

def user_look_for_car_filter_min_year_step(message):
    global year_min
    year_min = message.text
    try:
        int(year_min)
        if len(year_min) == 4 and int(year_min) >= 1950 and year_min.isdigit():
            msg = bot.send_message(message.chat.id, "Ok! Write maximal year.")
            bot.register_next_step_handler(msg, user_look_for_car_filter_max_year_step)
        else:
            msg = bot.send_message(message.chat.id, "You must to write integer!"
                                                    "\nYear must to be more or equal 1950"
                                                    "\nand year must to be less or equal 2021."
                                                    "\nMinimal year must to be less or equal maximal year!"
                                                    "\nOk! Write minimal year.")
            bot.register_next_step_handler(msg, user_look_for_car_filter_min_year_step)
    except Exception:
        msg = bot.send_message(message.chat.id, "You must to write integer!"
                                                "\nYear must to be more or equal 1950"
                                                "\nand year must to be less or equal 2021."
                                                "\nMinimal year must to be less or equal maximal year!"
                                                "\nOk! Write minimal year.")
        bot.register_next_step_handler(msg, user_look_for_car_filter_min_year_step)

def user_look_for_car_filter_max_year_step(message):
    global year_min
    global year_max
    year_max = message.text
    try:
        int(year_max)
        if len(year_max) == 4 and int(year_max) <= 2021 and year_max.isdigit() and (int(year_max) >= int(year_min)):
            bot.send_message(message.chat.id, f"Ok! \nYour filter:\nyear min: {year_min}\nyear max: {year_max}")
            bot.send_message(message.chat.id, f"Wait please! Data is loading.", reply_markup=hideBoard)
            global what_model_do_you_want
            global list_models

            sql = "SELECT COUNT(*) FROM all_сars " \
                  "WHERE year >= %s and year <= %s"
            year = (year_min, year_max,)
            mycursor.execute(sql, year)
            myresult = mycursor.fetchall()
            print(myresult)

            sql = "SELECT country, city, title, description, year, cost, link   FROM All_сars\
                                              WHERE cost = (SELECT MIN(cost) FROM All_сars)"
            mycursor.execute(sql)
            myresult_min = mycursor.fetchone()
            print(myresult_min)

            sql = "SELECT country, city, title, description, year, cost, link   FROM All_сars\
                                                      WHERE cost = (SELECT MAX(cost) FROM All_сars)"
            mycursor.execute(sql)
            myresult_max = mycursor.fetchone()
            print(myresult_max)
            bot.send_message(message.chat.id, f"Your choice:"
                                              f"\n{your_choice['Brand']}"
                                              f"\n{your_choice['Model']}"
                                              f"\nOk! Total listings {myresult[0][0]}.")
            bot.send_message(message.chat.id,
                             f"\nMIN. cost:\n{myresult_min[0]} \n{myresult_min[1]} \n{myresult_min[2]} \n{myresult_min[3]} \n{myresult_min[4]} г. \n{myresult_min[5]} $ \n{myresult_min[6]}")
            bot.send_message(message.chat.id,
                             f"\nMAX. cost:\n{myresult_max[0]} \n{myresult_max[1]} \n{myresult_max[2]} \n{myresult_max[3]} \n{myresult_max[4]} г. \n{myresult_max[5]} $ \n{myresult_max[6]}")
            msg = bot.send_message(message.chat.id, f"You can to see all listings"
                                                    f"\nin blocks of 5 items."
                                                    f"\nAlso you can use filter."
                                                    f"\nCOST: from... to..."
                                                    f"\nYEAR: from... to..."
                                                    , reply_markup=markup_watch_filter)
            bot.register_next_step_handler(msg, user_look_for_car_step)
        else:
            msg = bot.send_message(message.chat.id, "You must to write integer!"
                                                    "\nYear must to be more or equal 1950"
                                                    "\nand year must to be less or equal 2021."
                                                    "\nMinimal year must to be less or equal maximal year!"
                                                    "\nOk! Write maximal year.")
            bot.register_next_step_handler(msg, user_look_for_car_filter_max_year_step)
    except Exception:
        msg = bot.send_message(message.chat.id, "You must to write integer!!!"
                                                "\nYear must to be more or equal 1950"
                                                "\nand year must to be less or equal 2021."
                                                "\nMinimal year must to be less or equal maximal year!"
                                                "\nOk! Write maximal year.")
        bot.register_next_step_handler(msg, user_look_for_car_filter_max_year_step)

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

