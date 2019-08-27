from flask import Flask, render_template, redirect, url_for
from datetime import timedelta
import time
import pymysql

app = Flask(__name__)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = timedelta(seconds=1) 

@app.route("/index/")
def index():
	if page==0:
		game = game_list[:100]
	elif page==1:
		game = game_list[100:200]
	elif page==2:
		game = game_list[200:300]
	else:
		game = game_list[300:]
	return render_template("index.html", game=game, time=time.strftime("%Y.%m.%d-%H:%M:%S"))

@app.route("/page/<string:name>")
def flip(name):
	global page
	if name == "Next":
		page += 1
	else:
		page -= 1
	return redirect(url_for("index"))



def sql_query():
	conn = pymysql.connect(
		db="4399",
		host="localhost",
		user="root",
		passwd="your_password",
		port=3306,
		charset="utf8",
		)
	cur = conn.cursor()
	cur.execute("SELECT * FROM games")
	gamelist = cur.fetchall()
	return gamelist

if __name__ == '__main__':
	page = 0
	game_list = sql_query()
	app.run(debug=True)
