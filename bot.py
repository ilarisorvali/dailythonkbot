from core import *


if __name__ == "__main__":
    image_url = f'https://external.api.yle.fi/v1/teletext/images/895/1.png?app_id={APP_ID}&app_key={APP_KEY}'
    print(image_url)
    local_filename = 'downloaded_image.jpg'
    
    download_image(image_url, local_filename)
    
    post_image_to_channel(CHANNEL_ID, local_filename, SLACK_BOT_TOKEN, "✨Päivän Ajatus✨")
