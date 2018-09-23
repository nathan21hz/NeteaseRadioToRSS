import urllib
import urllib.request
import os
import json
import re
import PyRSS2Gen
import datetime

from os import path,system

headers = {"Cookie": "appver=1.5.0.75771",
"Referer":"http://music.163.com/",
"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36"}

radio_id = "350450350"

radio_url = "https://music.163.com/#/radio/?id="
radio_info_url = "http://musicapi.leanapp.cn/dj/detail?rid="
radio_program_url = "http://musicapi.leanapp.cn/dj/program?rid="
audio_url = "http://music.163.com/song/media/outer/url?id="
program_url = "https://music.163.com/#/program?id="

request = urllib.request.Request(url=radio_info_url+radio_id,headers=headers)
response = urllib.request.urlopen(request)
list_page = response.read().decode("utf-8")
page_json = json.loads(list_page)
info = page_json["djRadio"]

request = urllib.request.Request(url=radio_program_url+radio_id,headers=headers)
response = urllib.request.urlopen(request)
list_page = response.read().decode("utf-8")
page_json = json.loads(list_page)
programs = page_json["programs"]

item_list = []
for program in programs:
	temp_item = PyRSS2Gen.RSSItem(
		title = program["name"],
		link = 	program_url+str(program["id"]),
		description = program["description"],
		pubDate = datetime.datetime.fromtimestamp(int(int(program["createTime"])/1000)),
		guid = "netease_"+str(program["id"]),
		enclosure = PyRSS2Gen.Enclosure(
			url = audio_url+str(program["mainSong"]["id"])+".mp3",
			length = program["mainSong"]["bMusic"]["size"],
			type = "audio/mpeg"
			)
		)
	item_list.append(temp_item);

rss = PyRSS2Gen.RSS2(  
	title = info["name"],  
	link = radio_url+radio_id,  
	description = info["desc"], 
	language = "zh_CN",
	image = PyRSS2Gen.Image(
		url = info["picUrl"],
		title = info["name"],
		link = radio_url+radio_id
	),
	pubDate = datetime.datetime.fromtimestamp(int(int(info["lastProgramCreateTime"])/1000)),
	lastBuildDate = datetime.datetime.now(),
	items = item_list
)

rss.write_xml(open(radio_id+".xml", "w",encoding='utf-8'),encoding='utf-8')
