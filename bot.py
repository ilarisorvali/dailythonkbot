import requests
import os
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
from dotenv import load_dotenv

load_dotenv()

APP_ID = os.getenv('APP_ID')
APP_KEY = os.getenv('APP_KEY')
SLACK_BOT_TOKEN = os.getenv('SLACK_BOT_TOKEN')
CHANNEL_ID = os.getenv('CHANNEL_ID')

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

def post_image_to_slack(channel_id, filename):
    client = WebClient(token=SLACK_BOT_TOKEN)
    try:
        response = client.files_upload_v2(
            channels=channel_id,
            file=filename,
            title="✨Carpe Diem✨",
        )
        print(f"Image posted to Slack: {response['file']['permalink']}")
    except SlackApiError as e:
        print(f"Error uploading image: {e.response['error']}")

if __name__ == "__main__":
    image_url = f'https://external.api.yle.fi/v1/teletext/images/895/1.png?app_id={APP_ID}&app_key={APP_KEY}'
    print(image_url)
    local_filename = 'downloaded_image.jpg'
    
    # Download the image locally (testing)
    #download_image(image_url, local_filename)
    
    # Post the image to Slack
    post_image_to_slack(CHANNEL_ID, local_filename)
