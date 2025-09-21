# Dailythonkbot

Dailythonkbot is a python script to upload images from Yle tekstitv to Slack with a Slack bot user.




## Secrets setup
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
to post this weeks(changes on wednesday btw) recipes page and subpages to target CHANNEL_ID channel or

```python
python ajatus.py
```
to post the daily thought to target CHANNEL_ID channel.


## Automation

### Setup
By far the easiest way to schedule message sending is by building the project into a container and running it with Podman as a systemd service. We will focus on Podman [Quadlets](https://docs.podman.io/en/stable/markdown/podman-systemd.unit.5.html).

Run the following command in the cloned repository folder to build the container for podman/systemd to use, you can choose the image name freely (in this guide tekstitv):
```docker
podman build -t teksti .
```

Then running the container with the name we chose earlier as a scheduled systemd service is done with a systemd container unit and a timer. The container unit is a Podman Quadlet file. This is explained below.

daily-thought.container:
```ini
[Unit]
Description=Daily thought to slack
After=network.target

[Container]
Image=tekstitv
Exec=ajatus.py
EnvironmentFile=/home/ilari/dailythonkbot/.env
```
As you can see the container is started with the python file ajatus.py as the starting parameter. This simply executes the ajatus.py (post the daily thought to slack) once and then the container exits.

Path to the .env file can also be changed if you wish to keep it somewhere else, but be sure your user account has read access to it.

The recipe posting unit file is exactly the same except replace ajatus.py with recipes.py.

daily-thought.timer:
```ini
[Unit]
Description=Run dailythonkbot ajatus every day at 08:00 AM
Wants=time-sync.target
After=time-sync.target

[Timer]
OnCalendar=*-*-* 08:00:00
```

The above timer configuration fires the timer every day at 08:00. (Host machine time, be sure to **check the server timezone** before enabling the timer service).

The recipe posting timer file is exactly the same except replace the OnCalendar with a different time, once a week on Wednesdays at 12:00 is fine as the recipes have changed then from last weeks recipes.

It's convenient for the timer and container files to have same names like recipes.container and recipes.timer, because then systemd can automatically associate the timer to the .container file. Otherwise you'll have to manually specify in the timer what unit file you want to start with the timer.

Create the ajatus.container and recipes.container unit files in ~/.config/containers/systemd and the corresponding .timer file in ~/.config/systemd/user.

With a .container unit and .timer file created under their respective folders and the project container image built we can proceed to test and enable the services.

This is the general command to start user-level systemd services:

```bash
systemctl --user start name-of-service-unit.service
```
The --user flag makes the systemd service run at user-level instead of as a root level service. There is no need to run dailythonkbot as a root level service.

Podman Quadlet files are generated into systemd services on system boot and when
```bash
systemctl daemon-reload
```
command is run. Run the command above now.

In your .env file choose a CHANNEL_ID that you wish to use for testing purposes.

### Testing
All of the examples assume the unit files are named ajatus.container, recipes.container, ajatus.timer and recipes.timer.

Run the generated container unit once with the following command
```bash
systemctl --user start ajatus.service
```
You should now see a message with the Yle teksti-tv image posted on the chosen channel.

Try the recipes as well
```bash
systemctl --user start recipes.service
```
and now you should see the recipe page first image posted on the channel and subpages in the image thread. (There is currently a bug where subpages might get posted in incorrect order!)

To use the timer units simply enable the timer with
```bash
systemctl --user enable name-of-timer.timer
```
Do **NOT** enable the recipes.service or ajatus.service units directly because they will then start every time the system boots.

### Troubleshooting
If you encounter problems with the automation a good way to check for errors is
```bash
journalctl --user -u name-of-service.service
```
which will show you systemd logs about a particular service.

Most common errors result from incorrect .env variables (see [Secrets setup](#secrets-setup)).

## License

[MIT](https://choosealicense.com/licenses/mit/)
