#!/usr/bin/python



import time
import os
import urllib
import urllib2
import cookielib
import httplib
import bs4
import re

import mydb




def get_timeout_date():
	date=time.strftime("%Y-%m-%d", time.localtime(time.time()-7*86400))
	return date


class clear():
	def __init__(self, url, dbname):
		self.db = mydb.MyDb(ip = "127.0.0.1", user = "root", passwd = "liliang", dbname = dbname)
		self.ck = cookielib.CookieJar()
		self.handler = urllib2.HTTPCookieProcessor(self.ck)
		self.opener = urllib2.build_opener(self.handler)
		self.url = url	

	def clear_link_info(self):
		try:
			response = self.opener.open(self.url)
		except:
			return	
		self.db.cursor.execute("select link from link_info")
		results = self.db.cursor.fetchall()
		for row in results:
			link = row[0]
			try:
				re = self.opener.open(link)
			except:
				try:	
					reponse = self.opener.open(self.url)
				except:
					return

				time.sleep(3)
				try:
					 re = self.opener.open(link)
				except:
					self.db.cursor.execute("delete from link_info where link=%s",link)
					continue

			status = re.get_code()
			if(status != 200):
				self.db.cursor.execute("delete from link_info where link=%s",link)
				continue
			read = re.read()
 			soup = bs4.BeautifulSoup(read)
			goods = soup
			for ele in soup.find_all("div"):
				if ele.attrs.has_key("class") and "main" in ele.attrs['class']:
					goods = ele
					break
			for ele in goods.find_all("div"):
				if ele.attrs.has_key("class") and "item-box" in ele.attrs['class']:
					goods = ele
					break
			####get goods_name
			for ele in goods.find_all("h3"):
				if ele.attrs.has_key("class") and "item-title" in ele.attrs['class']:
					goods_name = ele.text
			
			try:
				####get goods_id
				goods_id = goods.attrs["data-tid"]
				continue
			except:
				self.db.cursor.execute("delete from link_info where link=%s",link)
	
	def clear_statistic(self):
		date = get_timeout_date()
		self.db.cursor.execute("delete from statistic where time < %s",date)	



if __name__ == "__main__":
	cl = clear(url="http://www.meilishuo.com", dbname = "mls")
	cl.clear_link_info()
	cl.clear_statistic()
