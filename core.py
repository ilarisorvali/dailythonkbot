import os
import requests
import time
from dotenv import load_dotenv
from slack_sdk import WebClient
from slack_sdk.web import SlackResponse

load_dotenv(override=True)

APP_ID = os.getenv('APP_ID')
APP_KEY = os.getenv('APP_KEY')
SLACK_BOT_TOKEN = os.getenv('SLACK_BOT_TOKEN')
CHANNEL_ID = os.getenv('CHANNEL_ID')
FILE_FOLDER = os.getenv("FILE_FOLDER")

client = WebClient(token=SLACK_BOT_TOKEN)

# Download the image locally
def download_image(image_url, local_filename):
    if not FILE_FOLDER:
        print("IMAGE_SAVE_PATH not set in .env file")
        return
    full_path = os.path.join(FILE_FOLDER, local_filename)

    # Download the image from the URL
    response = requests.get(image_url)
    if response.status_code == 200:
        # Save the image locally
        with open(full_path, 'wb') as file:
            file.write(response.content)
        print(f"Image downloaded: {local_filename}")
    else:
        print(f"Failed to download image. Status code: {response.status_code}")


def post_image_to_channel_v2(channel_id, filename, title, initial=None, thread=None) -> str | None:
    file_path = os.path.join(FILE_FOLDER, filename)
    file_size = os.stat(file_path).st_size

    #May be used later to get thread_ts with file_id if replies are needed
    info = None
    thread_id = None
    
    #Get url where to upload file
    url = client.files_getUploadURLExternal(filename=filename, length=file_size)
    upload_url = url["upload_url"]
    file_id = url["file_id"]
    
    #Open file and upload to Slack upload url
    with open(file_path, "rb") as file_content:
        
        postresponse = requests.post(upload_url, files={"file": file_content})

    #Complete the file upload and post to channel, may be replied to a thread with threads thread_ts    
    complete_response = client.files_completeUploadExternal(
            files=[{"id": file_id, "title": title}],
            channel_id=channel_id,
            thread_ts=thread,
            initial_comment=initial
        )
    
    #Dirty hack to make sure that uploaded thread start image gets a thread_ts from the server
    #FIXME idk make a better implementation (proper utils folder?)
    if (not thread):
        time.sleep(5)
        info = client.files_info(file=file_id)
        thread_id = info["file"]["shares"]["public"][channel_id][0]["ts"]

    return(thread_id) 

#Find out how many "subpages" a teksti-tv page has
def get_subpage_count(page) -> int:
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

#Post pages subpages, if it has any
#FIXME make a better implementation of posting a page and subpages eg. post single page & post page and subpages as replies
def post_subpages(page, thread):
    subpage_count = get_subpage_count(page)
    print(subpage_count)

    #Starts from 2 because page 1 is the main page of the section
    for i in range(2, subpage_count + 1):
        image_url = f"https://external.api.yle.fi/v1/teletext/images/{page}/{i}.png?app_id={APP_ID}&app_key={APP_KEY}"
        local_filename = f"page_{page}_subpage_{i}.png"
        # Download the image
        download_image(image_url, local_filename)

        # Post the image to Slack
        text = f"Page {page}, Subpage {i}"
        post_image_to_channel_v2(CHANNEL_ID, local_filename, text, thread=thread)