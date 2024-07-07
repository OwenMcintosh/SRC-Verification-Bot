# Discord - Speedrun.com user verification
This is a discord bot that helps verify, and therefore link, users to their speedrun.com account. This is useful for preventing bad actors, or server brigading.

## Usage

This project does not contain any discord API keys, therefore you'll have to make your own bot & get your own discord API key [here.](https://discord.com/developers/applications) Once you've got your bot set up, and have your API key, the bot can be ran by creating a .env file in the root directory, which'll hold the environment variable "DISCORD_API_KEY" and your API key in the following format:

`DISCORD_API_KEY="(YOUR_API_KEY)"`

This project makes use of the speedruncompy API wrapper for Speedrun.com's V2 API by [Jamie](https://github.com/ManicJamie) and thus is limited to python versions 3.11 and newer, due to this dependency. Please make sure to give her your support! :) 

## Adaptable Variables:

At the top of the VerifyUser cog file, you'll find a few variables that can be changed to fit the purpose of your needs. These variables are as follows;

- discordTimeCheckInSeconds
- verifiedRoleName
- monthCheck
- gameList

These variables are sufficiently commented for their uses.

## Known Issues:

- Speedrun.com discord social links may use the old 4 digit discriminator format. These legacy usernames aren't currently available to the discord botting API, and may never be as Discord aims to step away from the discriminator formatting.

- Only checks for verified runs, rather than currently pending runs. This is currently a mystery to the Speedrun.com V2 API that the community haven't figured out yet. This will be fixed ASAP.
