import discord, sqlite3

con = sqlite3.connect('obdm_images.sqlite3')
cur = con.cursor()
img_sql = "INSERT INTO obdm_img (hyperlink, name) VALUES (?, ?)"

discord_bot_token = 'Found at https://discordapp.com/developers/applications/'
client = discord.Client()

@client.event
async def on_ready():
    channel = client.get_channel(646000041567453184)
    messages = await channel.history().flatten()
    for message in messages:
        try:
            x =  message.attachments
            for z in x:
                cur.execute(img_sql, (z.url, ''))
                con.commit()
        except sqlite3.IntegrityError:
            pass
        except Exception as e:
            print('Discord ', e)

client.run(discord_bot_token)