from slackclient import SlackClient
import json, slack, sqlite3

Slack_Access_Token = 'xoxp-SOMETHING FIND YOUR OWN AT API.SlACK.COM'
Slack_Bot_Token = 'xoxb-SOMETHING FIND YOUR OWN AT API.SlACK.COM'
Slack_Channel = 'Right click the channel and locate it within the link'

con = sqlite3.connect('obdm_images.sqlite3')
cur = con.cursor()
img_sql = "INSERT INTO obdm_img (hyperlink, name) VALUES (?, ?)"

def sql_commit(x):
    cur.execute(img_sql, (x, ''))
    con.commit()

def img_list(imgs):
    for i in imgs.get('messages'):
        try:
            if i.get('attachments') and i.get('attachments')[0].get('image_url') is not None:
                sql_commit(i.get('attachments')[0].get('image_url'))
            elif i.get('files'):
                sql_commit(i.get('files')[0].get('url_private'))
        except sqlite3.IntegrityError:
            pass
        except Exception as e:
            print('Error Slack 1 ', type(e))

def img_list_two(i, x):
    if x == 0:
        sql_commit(i.get('files')[0].get('url_private'))
    else:
        sql_commit(i.get('message').get('files')[0].get('url_private'))

sc = SlackClient(Slack_Access_Token)
x = sc.server.api_call("channels.history", channel=Slack_Channel).decode()
slack_images = img_list(json.loads(x))
rtm_client = slack.RTMClient(token=Slack_Bot_Token)

@slack.RTMClient.run_on(event='message')
def say_hello(**payload):
    data = payload['data']
    if data['channel'] == Slack_Channel:
        try:
            if 'files' in data.keys() and data.get('files')[0].get('url_private') is not None:
                img_list_two(data, 0)
            elif 'message' in data.keys():
                img_list_two(data, 1)
        except Exception as e:
            print('Error Slack 2 ', e)

