#!/usr/bin/env python          
# -*- coding:utf-8 -*-

import requests
import time 
import os
import subprocess
import re
from bs4 import BeautifulSoup
from PIL import Image, ImageFont, ImageDraw
import random

user_agent = [
	"Mozilla/5.0 (compatible; Baiduspider/2.0; +http://www.baidu.com/search/spider.html)",
	"Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; AcooBrowser; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
	"Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0; Acoo Browser; SLCC1; .NET CLR 2.0.50727; Media Center PC 5.0; .NET CLR 3.0.04506)",
	"Mozilla/4.0 (compatible; MSIE 7.0; AOL 9.5; AOLBuild 4337.35; Windows NT 5.1; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
	"Mozilla/5.0 (Windows; U; MSIE 9.0; Windows NT 9.0; en-US)",
	"Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Win64; x64; Trident/5.0; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 2.0.50727; Media Center PC 6.0)",
	"Mozilla/5.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 1.0.3705; .NET CLR 1.1.4322)",
	"Mozilla/4.0 (compatible; MSIE 7.0b; Windows NT 5.2; .NET CLR 1.1.4322; .NET CLR 2.0.50727; InfoPath.2; .NET CLR 3.0.04506.30)",
	"Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN) AppleWebKit/523.15 (KHTML, like Gecko, Safari/419.3) Arora/0.3 (Change: 287 c9dfb30)",
	"Mozilla/5.0 (X11; U; Linux; en-US) AppleWebKit/527+ (KHTML, like Gecko, Safari/419.3) Arora/0.6",
	"Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.1.2pre) Gecko/20070215 K-Ninja/2.1.1",
	"Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN; rv:1.9) Gecko/20080705 Firefox/3.0 Kapiko/3.0",
	"Mozilla/5.0 (X11; Linux i686; U;) Gecko/20070322 Kazehakase/0.4.5",
	"Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.8) Gecko Fedora/1.9.0.8-1.fc10 Kazehakase/0.5.6",
	"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11",
	"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_3) AppleWebKit/535.20 (KHTML, like Gecko) Chrome/19.0.1036.7 Safari/535.20",
	"Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; fr) Presto/2.9.168 Version/11.52"
]

HEADER = {
'User-Agent': random.choice(user_agent),  # 浏览器头部
'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3', # 客户端能够接收的内容类型
'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8', # 浏览器可接受的语言
'Connection': 'keep-alive', # 表示是否需要持久连接
'cookie':'MUID=225D735E7B5E63B7034A7D5F7F5E6026; SRCHD=AF=NOFORM; SRCHUID=V=2&GUID=DD61EE30B05A4FC38EE40AFC2CD365CB&dmnchg=1; MUIDB=225D735E7B5E63B7034A7D5F7F5E6026; _UR=MC=1; ENSEARCH=BENVER=1; SRCHUSR=DOB=20191030&T=1572607372000; ULC=P=1AF53|23:5&H=1AF53|54:6&T=1AF53|51:6:99; _EDGE_S=SID=0ABB5541A8F2602D1FCD5B4DA93A61DC; _SS=SID=0ABB5541A8F2602D1FCD5B4DA93A61DC&bIm=382&HV=1573007230; ipv6=hit=1573010829662&t=4; SRCHHPGUSR=CW=583&CH=702&DPR=2&UTC=480&WTS=63708604028'
}

def get_wallpaper():
	URL = "https://www.bing.com/"

	html = requests.get(URL,headers=HEADER).text
	soup = BeautifulSoup(html, 'lxml')
	img_ul = soup.find_all('link', {"id": "bgLink"})

	# find the text
	# '"copyright":"Clarée Valley, Massif des Cerces, Hautes-Alpes, France (© Franck Guiziou/Alamy)","copyrightlink"'
	pattern = r'\"copyright\"\:\".*\"\,\"copyrightlink\"'
	pattern = re.compile(pattern)
	result = pattern.findall(html)
	image_text = ''
	for i in result:
		image_text = i.replace('"copyright":"', '').replace('","copyrightlink"', '').replace('© ', '')

	filename = ''
	# save file
	for ul in img_ul:
	    r = requests.get(URL + ul['href'], stream=True)
	    filename = '/Users/shinkeika/Pictures/net.neolib.BingDailyWallpaper/' + time.strftime('%Y_%m_%d_%H',time.localtime(time.time())) + '.jpeg'
	    with open(filename, 'wb+') as f:
	        for chunk in r.iter_content(chunk_size=128):
	            f.write(chunk)
	    print('Saved %s' % filename)

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