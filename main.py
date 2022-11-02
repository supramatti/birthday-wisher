import glob
import smtplib
import datetime
import random
import pandas
import os

MY_EMAIL = "youremail"
PASSWORD = "yourpassword"
dt = datetime.datetime

try:
    with open("birthdays.csv") as file:
        birthdays = pandas.read_csv(file).to_dict(orient="records")
except FileNotFoundError:
    print("File not found")

letters_list = []
path = 'letter_templates/'
for filename in glob.glob(os.path.join(path, '*.txt')):
    try:
        with open(filename, "r") as file:
            letters_list.append(file.read())
    except FileNotFoundError:
        print("File not found")

day = dt.now().day
month = dt.now().month
email_to_send = ''
name_to_send = ''
has_mail_to_send = False
letter = random.choice(letters_list)

for item in birthdays:
    if item['day'] == day and item['month'] == month:
        email_to_send = item['email']
        name_to_send = item['name']
        has_mail_to_send = True

if has_mail_to_send:
    letter = letter.replace('[NAME]', name_to_send)
    with smtplib.SMTP(host="smtp.gmail.com", port=587) as connection:
        connection.starttls()
        connection.login(user=MY_EMAIL, password=PASSWORD)
        connection.sendmail(from_addr=MY_EMAIL, to_addrs=email_to_send,
                            msg=f"Subject:Happy birthday!\n\n{letter}")
