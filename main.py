from flask import Flask, render_template
import sqlite3, subprocess

con = sqlite3.connect('obdm_images.sqlite3', check_same_thread=False)
cur = con.cursor()

def create_table():
    obdm_sql = """
        CREATE TABLE obdm_img (
            hyperlink text PRIMARY KEY,
            name text)"""
    cur.execute(obdm_sql)

#create SQL table if doesn't exist
cur.execute(''' SELECT count(name) FROM sqlite_master WHERE type='table' AND name='obdm_img' ''')
if cur.fetchone()[0]==1 :
	print('Table exists.')
else :
	create_table()

app = Flask(__name__)
@app.route('/')
def index():
    cur.execute('SELECT * FROM obdm_img')
    rows = cur.fetchall()
    images = [[row[0], rows.index(row)] for row in rows]
    return render_template('obdm.html', title='Home', img_list=sorted(images, key = lambda x: x[1], reverse=True))

process1 = subprocess.Popen(["python", "discord_bot.py"])
process2 = subprocess.Popen(["python", "slack_bot.py"])
app.run()