import os
import requests
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError

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
def post_image_to_slack(channel_id, filename, bot_token):
    client = WebClient(token=bot_token)
    try:
        response = client.files_upload_v2(
            channels=channel_id,
            file=filename,
            title="✨Carpe Diem✨",
        )
        print(f"Image posted to Slack: {response['file']['permalink']}")
    except SlackApiError as e:
        print(f"Error uploading image: {e.response['error']}")