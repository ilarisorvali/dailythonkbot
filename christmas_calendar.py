from core import *


if __name__ == "__main__":
    image_url = f'https://external.api.yle.fi/v1/teletext/images/831/1.png?app_id={APP_ID}&app_key={APP_KEY}'
    local_filename = 'christmas_calendar.jpg'
    
    download_image(image_url, local_filename)
    
    post_image_to_channel_v2(CHANNEL_ID, local_filename, "Joulukalenteri")