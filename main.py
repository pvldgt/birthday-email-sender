import datetime as dt
import pandas as pd
import random
import os
import smtplib
# create your own personal_data file with the my_email and _my_password variables
from personal_data import my_email, my_password

letter_to_send = ""
email_to_send = ""

# read the csv file with birthday info into a data frame
birthdays = pd.read_csv("birthdays.csv")
# transform the data frame into a dictionary
birthday_dict = birthdays.to_dict(orient="records")

# check the current day and month
now = dt.datetime.now()
today_month = now.month
today_day = now.day

# go through every entry in the dictionary and see if the date matches today
for entry in birthday_dict:
    if entry["month"] == today_month and entry["day"] == today_day:
        # if it does, pick a random letter from letter templates
        random_letter = random.choice(os.listdir("letter_templates"))
        with open(f"letter_templates/{random_letter}") as letter_file:
            letter_text = letter_file.read()
        # replace the [NAME] with the person's actual name
        letter_to_send = letter_text.replace("[NAME]", entry["name"])
        # get the email of the recipient
        email_to_send = entry["email"]

# send the letter generated above to that person's email address.
with smtplib.SMTP("smtp.gmail.com", port=587) as connection:
    connection.starttls()
    connection.login(user=my_email, password=my_password)
    connection.sendmail(from_addr=my_email,
                        to_addrs=email_to_send,
                        msg=f"Subject: Happy Birthday!\n\n{letter_to_send}")
