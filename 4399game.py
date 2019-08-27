#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
from lxml import etree
import re
import pymysql

host_url = "http://www.4399.com"
hw_suffix = "/flash/gamehw.htm"

def html_data(url):
	html_r = requests.get(url)
	return html_r.content

def get_result():
	result_list = []
	html_r =  html_data(host_url+hw_suffix)
	root = etree.HTML(html_r)
	game_list = root.xpath("//*[@id='skinbody']/div[6]/ul/li")
	for item in game_list:
		# href title src type
		game_url_cur = host_url + item.xpath("a/@href")[0]
		game_url = get_url(game_url_cur)
		if not game_url:
			continue
		game_alt = item.xpath("a/b/text()")[0]
		try:
			game_src = item.xpath("a/img/@src")[0]
		except:
			game_src = item.xpath("a/img/@lz_src")[0]
		game_type = item.xpath("em/a/text()")[0]
		game_info = game_alt, game_url, game_src, game_type
		result_list.append(game_info)
	return result_list

def get_url(url):
	try:
		html_r = html_data(url)
	except:
		return False
	reg = r'/js/server(.*?).js'
	server = re.findall(reg, html_r.decode("gbk"))
	try: 
		if server != None:
			server = server[0]
			reg = r'_strGamePath="(.*?)"'
			swfurl = re.findall(reg, html_r.decode("gbk"))[0]
			return 'http://%s.4399.com/4399swf%s' % (server, swfurl)
	except:
		pass

def write_database(games):
	conn = pymysql.connect(
		db="4399",
		host="localhost",
		user="root",
		passwd="your_password",
		port=3306,
		charset="utf8"
		)
	cur = conn.cursor()
	for game in games:
		cur.execute("insert into games VALUES(NULL,'%s','%s','%s','%s')" % (game[0], game[1], game[2], game[3]))
	cur.close()
	conn.commit()
	conn.close()
	
if __name__ == '__main__':
	
	games = get_result()
	# print(len(games))
	write_database(games)