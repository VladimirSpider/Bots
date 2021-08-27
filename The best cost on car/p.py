import datetime
from dateutil.relativedelta import relativedelta
dt_now = datetime.datetime.now()
print(dt_now)

current_date = datetime.date.today()
print(current_date)

current_date = datetime.datetime.now().date()
print(current_date)

current_time = datetime.datetime.now().time()
print(current_time)

my_date_birthday = datetime.date(1993, 10, 21)
print(my_date_birthday)

year = 1993
month = 10
day = 21
my_date_birthday = datetime.date(year, month, day)
print(my_date_birthday)

print(my_date_birthday.year)

print((current_date - my_date_birthday).days)

print("Age:", relativedelta(current_date, my_date_birthday).years)


