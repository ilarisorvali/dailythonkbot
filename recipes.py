import os
from core import *
from dotenv import load_dotenv

load_dotenv(override=True)

APP_ID = os.getenv('APP_ID')
APP_KEY = os.getenv('APP_KEY')
SLACK_BOT_TOKEN = os.getenv('SLACK_BOT_TOKEN')
CHANNEL_ID = os.getenv('CHANNEL_ID')

if __name__ == "__main__":
    page_number = 811
    image_url = f'https://external.api.yle.fi/v1/teletext/images/{page_number}/1.png?app_id={APP_ID}&app_key={APP_KEY}'
    print(image_url)
    local_filename = 'recipe_image.jpg'

    download_image(image_url, local_filename)

    thread: str | None = None
    resp = post_image_to_channel(CHANNEL_ID, local_filename, SLACK_BOT_TOKEN, "Viikon reseptit")
    if resp is not None:
        thread = resp.get("ts")

    post_subpages(page_number, thread=thread)
