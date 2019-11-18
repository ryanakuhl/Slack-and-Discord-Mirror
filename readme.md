Discord_bot.py and Slack_bot.py monitor a discord and slack channel respectively for images, then saves them to a db. Main reads the db and offers a Flask web framework.

Currently, the Discord bot only picks up file uploads. Slack sees file uploads and image links.

Requires a Discord Bot (https://discordapp.com/developers/applications/) and Slack App and bot (https://api.slack.com/apps)
