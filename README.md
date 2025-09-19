# Dailythonkbot

Dailythonkbot is a python script to upload images from Yle tekstitv to Slack with a Slack bot user.

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install foobar.

```bash
pip install foobar
```

## Setup
You need some variables set in the .env file to access the Yle tekstitv API and to use bot via Slack API for image posting.

```
#Yle API access keys
APP_ID=YOUR APP ID
APP_KEY=YOUR APP KEY

#Slack OAuth bot token
SLACK_BOT_TOKEN=YOUR SLACK BOT TOKEN

CHANNEL_ID=CHANNEL ID OF THE CHANNEL YOU WANT TO POST DAILY THOUGHT AND RECIPES IN
``` 
### Yle API keys

Getting Yle Teletext API keys is fairly trivial. See [here](https://developer.yle.fi/en/index.html) for instructions, [API tutorials](https://developer.yle.fi/tutorial-get-teletext-images/index.html) and documentation. You'll need app_id and app_key pair to authenticate to the service. 

(Be mindful of the rate limit 0 requests/second, 300 requests/hour and 7200 requests/day!)

### Slack bot and bot tokens
Slack bot setup and bot tokens are a bit complex and authentication protocol changes from time to time.

First (if you don't have an App or wish to create a new one) you need to go to [Your Apps](https://api.slack.com/apps/) and create a new Slack App (Select button Create New App, From Scratch). Select the Slack workspace you wish your bot to exist in and a configuration page opens for the new App. From the side menu, navigate to OAuth & permissions page. Scroll down to scopes and add following scopes:

- channels:join
- chat:write
- files:read
- files:write

These are needed to upload files (our images) to channels. With these permissions and the bot token the app is ready to be installed into the Slack workspace. Scroll up and click the button "Install to (workspace you selected when creating the app)". 

After that you'll see the xoxb- token that is used to authenticate as the App.

From the basic information page you can setup App profile picture, description, etc. if you wish.

The bot currently uses a channel_id that can be found by opening Slack, right clicking the target channel and selecting "Channel details". Channel ID is at the bottom of the opening details window.

It is recommended to create a testing channel to Slack as not to disturb channels that are in use.

### All together
So now you should have
- APP_ID (Yle)
- APP_KEY (Yle)
- SLACK_BOT_TOKEN (Slack)
- CHANNEL_ID (Slack)


## Usage
Loading up all the secrets to the .env file you can run the script with 
```python
python recipes.py
```
to pos this weeks(changes on wednesday btw) recipes page and subpages to target CHANNEL_ID channel or

```python
python ajatus.py
```
to post the daily thought to target CHANNEL_ID channel.


## License

[MIT](https://choosealicense.com/licenses/mit/)
