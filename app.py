import os
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
from dotenv import load_dotenv

load_dotenv()
SECRET_ENV = os.getenv("SECRET_ENV")
client = WebClient(
    token=f"{SECRET_ENV}"
)

try:
    response = client.chat_postMessage(channel = "C06U0QC2TGE", text="WRITE_MESSAGE_HERE")

except SlackApiError as err:
    print(f"Error:{err.response["error"]}")
