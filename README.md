# Sajti's RA Presence

A little software which lets you share your RetroAchievements activity with your friends on Discord.

### Before you even consider downloading,
note that I have none to zero programming experience. I put this together in less than a week as a fun project/challenge, using Google, reading documentations, and asking Grok about how things work. The main inspiration was [RetroAchievements-Discord-Presence](https://github.com/XtremePrime/RetroAchievements-Discord-Presence), so huge credit to everyone working on it.

The source code looks like "meh," but at least I can read it clearly. There's almost no error handling. Written and tested on Windows, but I suppose it works on every operating system.

In the future, I might update this project, or I might not—who knows? However, I will appreciate any kind of advice, criticism, or feedback you have for me after using my program or checking the code. Maybe one day I will become a huge Python developer. Just maybe.

## Requirements
- Python3 with tkinter
- ```pip install -r requirements.txt```
  	- `configparser` https://pypi.org/project/configparser/
  	- `pypresence` https://pypi.org/project/pypresence/
  	- `pillow` https://pypi.org/project/pillow/
- From RetroAchievements, your username and your API key
- From Discord... well...

Here's the bad news: You will have to create an app at the Discord Developer Portal (https://discord.com/developers/applications/), give it a nice, unique name which will appear below your name as a "Playing" status. Don't worry if you mess up; you can modify the name of the app anytime. From there, you will need the ID of your app and the Bot token. Yes, you will need a bot token as well, for authentication. (To make sure your app ID is correct and scrape the app name for displaying on the UI.)

## Features

- Detailed Rich Presence on your Discord profile (name of the game, details about what you're currently doing in the game, icons, etc.)
- Two clickable buttons. One leads to the RA page of the game you're currently playing; the other leads to your RA profile (only others can see them). You can enable or disable them in the settings.
- A simple UI which tells you some information.

The displayed images on the UI are all clickable. The first one with your RA profile picture leads to your RA profile, the second next to it leads to the page of your Discord app (if you wish to modify the name), the gears obviously lead to settings, and if you click on the icon of your game, it leads you to its RA page.
To open the settings, the application will restart itself. I know it's bad design, but I couldn't come up with a better solution.
Note: If you modify your Discord app name while the program is running, to display the new name on Discord, you will need to restart the program manually.

## Usage
After installing the requirements and ensuring you have all the required data, simply launch `srp.pyw`. It greets you with a Settings window; fill it up with the required data, check the other options, and you're good to go. You can launch it from the terminal/cmd or whatever, but it doesn't print any useful information there.

## Screenshots
![1](https://github.com/user-attachments/assets/c0d18b82-6d45-4a7c-b792-533d99b90884)|![3](https://github.com/user-attachments/assets/8db38086-67b4-40d2-9015-592739ee7f0d)
---|---
![4](https://github.com/user-attachments/assets/368415bc-1d08-4e29-b8dd-16a4c2b28517)|![2](https://github.com/user-attachments/assets/45910a42-07ab-452a-94e8-ef5f42352753)


