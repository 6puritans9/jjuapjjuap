#!/usr/bin/env python3
import os
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
from dotenv import load_dotenv
from scrape_meal import get_weekly_dreamtower_meal
import datetime as dt
load_dotenv()
SECRET_ENV = os.getenv("SECRET_ENV")
client = WebClient(
    token=f"{SECRET_ENV}"
)

try:
    x = dt.datetime.now()
    print(x)
    today_meal = get_weekly_dreamtower_meal(x.weekday())
    if today_meal:
        response = client.chat_postMessage(channel = "C06U0QC2TGE", text=f'>*📅{today_meal["date"]}{today_meal["day"]}*\n>*점심 🥗*\n{today_meal["lunch"]}\n>*저녁🍲*\n{today_meal["dinner"]}')

except SlackApiError as err:
    print(f"Error:{err.response['error']}")
