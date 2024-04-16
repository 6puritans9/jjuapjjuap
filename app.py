#!/usr/bin/env python3
import os
import datetime as dt
from dotenv import load_dotenv
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
from scraper import get_weekly_dreamtower_meal

load_dotenv()
SLACK_TOKEN = os.getenv("SECRET_ENV")
DEFAULT_CHANNEL_ID = os.getenv("DEFAULT_CHANNEL_ID")  # Default fallback channel

client = WebClient(token=SLACK_TOKEN)


def get_channels():
    result = client.conversations_list()
    channels = result["channels"]
    valid_channel = []
    for channel in channels:
        if channel["is_member"]:
            valid_channel.append(channel)
    return valid_channel


def post_meal_to_channel(channels_list):
    try:
        current_time = dt.datetime.now()
        print(current_time)

        today_meal = get_weekly_dreamtower_meal(current_time.weekday())
        if today_meal:
            # Post the meal information to the specified Slack channel
            for each_channel in channels_list:
                response = client.chat_postMessage(
                    channel=each_channel["id"],
                    text=f'>*📅{today_meal["date"]}{today_meal["day"]}*\n>*점심*\n{today_meal["lunch"]}\n>*저녁*\n{today_meal["dinner"]}',
                )
        else:
            return

    except SlackApiError as err:
        print(f"Houston, we have a problem: {err}")


if __name__ == "__main__":
    channels = get_channels()
    post_meal_to_channel(channels)
