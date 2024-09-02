import os
import json
import requests
from dotenv import load_dotenv
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError

load_dotenv(override=True)

APP_ID = os.getenv('APP_ID')
APP_KEY = os.getenv('APP_KEY')
SLACK_BOT_TOKEN = os.getenv('SLACK_BOT_TOKEN')
CHANNEL_ID = os.getenv('CHANNEL_ID')

# Download the image locally
def download_image(image_url, local_filename):
    # Download the image from the URL
    response = requests.get(image_url)
    if response.status_code == 200:
        # Save the image locally
        with open(local_filename, 'wb') as file:
            file.write(response.content)
        print(f"Image downloaded: {local_filename}")
    else:
        print(f"Failed to download image. Status code: {response.status_code}")

# Post the image to Slack
def post_image_to_channel(channel_id, filename, bot_token, text):
    client = WebClient(token=bot_token)
    try:
        response = client.files_upload_v2(
            channels=channel_id,
            file=filename,
            title=text,
        )

        print(f"Image posted to Slack: {response['file']['permalink']}")
        
    except SlackApiError as e:
        print(f"Error uploading image: {e.response['error']}")

def post_images_to_thread():
    pass

def get_subpage_count(page):
    url = f"https://external.api.yle.fi/v1/teletext/pages/{page}.json?app_id={APP_ID}&app_key={APP_KEY}"

    try:
        response = requests.get(url)
        response.raise_for_status()
        json_data = response.json()

        subpage_count = int(json_data['teletext']['page']['subpagecount'])
        return(subpage_count)
    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")
    except KeyError as key_err:
        print(f"Key error occurred: {key_err}")
    except Exception as err:
        print(f"Other error occurred: {err}")

def post_subpages(page, ts):
    subpage_count = get_subpage_count(page)
    print(subpage_count)
    
    # Initialize thread timestamp
    thread_ts = None
    
    #Starts from 2 because page 1 is the main page of the section
    for i in range(2, subpage_count + 1):
        image_url = f"https://external.api.yle.fi/v1/teletext/images/{page}/{i}.png?app_id={APP_ID}&app_key={APP_KEY}"
        local_filename = f"page_{page}_subpage_{i}.png"
        
        # Download the image
        download_image(image_url, local_filename)
        
        # Post the image to Slack
        text = f"Page {page}, Subpage {i}"
        post_image_to_channel(CHANNEL_ID, local_filename, SLACK_BOT_TOKEN, text)

