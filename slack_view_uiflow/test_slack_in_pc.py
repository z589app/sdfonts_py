import requests
import json
import os
import re

url = "https://slack.com/api/channels.history"
token = os.environ['SLACK_TOKEN']
channel_id = os.environ['SLACK_CHANNEL_ID']

def main():
    payload = {
        "token": token,
        "channel": channel_id
        }
    response = requests.get(url, params=payload)

    json_data = response.json()
    messages = json_data["messages"]
    for i in sorted(messages, key=lambda mes: mes['ts'], reverse=True)[5::-1]:
        text = i['text']
        text = re.sub(r':[\w_]*:', "", text)
        print(text)

if __name__ == '__main__':
    print(token, channel_id)
    main()
