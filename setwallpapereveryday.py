#!/usr/bin/env python          
# -*- coding:utf-8 -*-

import requests
import time 
import os
import subprocess
import re
from bs4 import BeautifulSoup
from PIL import Image, ImageFont, ImageDraw



def get_wallpaper():
	URL = "https://www.bing.com"

	html = requests.get(URL).text
	soup = BeautifulSoup(html, 'lxml')
	img_ul = soup.find_all('link', {"id": "bgLink"})

	# save file
	for ul in img_ul:
	    r = requests.get(URL + ul['href'], stream=True)
	    filename = '/Users/shinkeika/Pictures/net.neolib.BingDailyWallpaper/' + time.strftime('%Y_%m_%d',time.localtime(time.time())) + '.jpeg'
	    with open(filename, 'wb+') as f:
	        for chunk in r.iter_content(chunk_size=128):
	            f.write(chunk)
	    print('Saved %s' % filename)
	# find the text
	pattern=r"\"copyright\"\:\".*\"\,\"copyrightlink\""
	pattern = re.compile(pattern)
	result = pattern.findall(html)
	for i in result:
	    image_text = i.replace('"copyright":"','').replace('","copyrightlink"','').replace('© ','')

	return filename,image_text


def drawtext(fn,it):
	im = Image.open(fn)  # 打开文件

	font = ImageFont.truetype('/Users/shinkeika/pythonproject/setwallpaper/simhei.ttf', 30)

	draw = ImageDraw.Draw(im)  # 修改图片

	x,y=(300,900)  #初始左上角的坐标

	draw.text((x,y), image_text, font=font)
	# im.show()
	im.save(fn)


SCRIPT = """/usr/bin/osascript<<END
tell application "Finder"
set desktop picture to POSIX file "%s"
end tell
END"""


def set_wallpaper(s):
    subprocess.Popen(SCRIPT % s, shell=True)


if __name__ == '__main__':
    img, image_text = get_wallpaper()
    if img:
    	drawtext(img, image_text)
    	set_wallpaper(img)