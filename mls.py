#!/usr/bin/python
#-*- coding: utf-8 -*-


import os
import time
import urllib
import urllib2
import cookielib
import httplib
import bs4
import re
import mydb
print "测试"

kind_no = {
	"shangyi":1
}


class MlsData():
	def __init__(self, url):
		self.url = self.__get_url__(url)
		self.ck = cookielib.CookieJar()
		self.handler = urllib2.HTTPCookieProcessor(self.ck)
		self.opener = urllib2.build_opener(self.handler)
		self.shangyi = []
		self.shangyi_pages = set()
		self.mydb = mydb.MyDb(ip="127.0.0.1",user="root",passwd="liliang",dbname="mls")
		self.shangyi_fail_pages = []
		self.opener.open("http://www.meilishuo.com/guang/catalog/dress?nid=210113&cata_id=2001000000000")
		urllib2.install_opener(self.opener)
		time.sleep(3)
	def __get_url__(self, url):
		if(url[0:4] != "http"):
			return "http://"+url
	def get_main_page(self):
		response = self.opener.open(self.url)
		read = response.read()
			
		self.main_page=bs4.BeautifulSoup(read)

	def get_shangyi_link(self):
		soup = self.main_page
		shangyis = soup.body.find_all("a",text=re.compile(u"上衣"))
		for ele in shangyis:
			url = self.url + ele['href']
			if url in self.shangyi:
				continue
			self.shangyi.append(url)
		print self.shangyi	
						
	def get_shangyi_page(self):
		frm_url = "http://www.meilishuo.com/guang/catalog/dress?nid=210113&cata_id=2001000000000"
		aj_url ="http://www.meilishuo.com/aj/getGoods/catalog?frame=%d&page=%d&view=1&word=0&cata_id=2001000000000&section=hot&price=all&nid=210113"
	 	bay_url = "http://www.meilishuo.com/aj/sale/bay_window"
		common_url = "http://www.meilishuo.com/aj/fullalert/dialog?time_type=1" 
		attach_url = "http://www.meilishuo.com/aj/getMsg/"	
		for page in range(0, 60):
			print "page=%d"%page
			link = frm_url + "&page=%d&frame=0"%page
				
			response = self.opener.open(link)
			print link
			read = response.read()
			soup = bs4.BeautifulSoup(read)
			scripts = soup.body.find_all("script")
			for ele in scripts:
				if "Meilishuo.config.p4p" in unicode(ele.string):
					#value.add(unicode(ele.string))
					items = re.findall("\"url\":\"/share/item/[0-9]+\?",unicode(ele.string))
					for item in items:
						goods_url = self.url + item.split(":\"")[1].strip()	
						self.shangyi_pages.add(goods_url)
						#print goods_url
						##self.get_goods_detail(goods_url)
				else:
					pass	
			
			try:
				self.operner.open(bay_url)
			except:
				print bay_url
				pass
			try:
				self.operner.open(common_url)	
			except:
				print common_url
				pass
			try:
				self.opener.open(attach_url)
			except:
				print attach_url
				pass
			
			for frame in range(1,11):
				ajurl = aj_url%(frame,page)
				try:
					response = self.opener.open(ajurl, timeout=5)
				except:
					print ajurl
					print "continue"
					continue
				read = response.read()
				items = re.findall("\"url\"\:\"\\\/share\\\/item\\\/[0-9]+\?", read)
				for item in items:
					item = item.replace("\\","")
					goods_url = self.url + item.split(":\"")[1].strip()
					#print item
					#print goods_url	
					self.shangyi_pages.add(goods_url)
		
			
					
		
					
				
	def get_frm_shangyi_page(self):
		value=set()
		shangyi = self.shangyi[0]
		for page in range(1,100):
			link = shangyi+"&page=%d"%page
			response = self.opener.open(link)
			read = response.read()
			soup = bs4.BeautifulSoup(read)
			scripts = soup.body.find_all("script")
			for ele in scripts:
				if "Meilishuo.config.p4p" in unicode(ele.string):
					value.add(unicode(ele.string))
		print value
		print len(value)
		for ele in value:
			items = re.findall("\"url\":\"/share/item/[0-9]+\?",ele)
			for item in items:
				#print item
				goods_url = self.url + item.split(":\"")[1].strip()	
				self.shangyi_pages.add(goods_url)
		
	
	def get_aj_shangyi_page(self):
		url = "http://www.meilishuo.com/aj/getGoods/catalog?frame=%d&page=%d&view=1&word=0&cata_id=2001000000000&section=hot&price=all&nid=210113"
		for page in range(0,55):
			for frame in range(1,11):
				ajurl = url%(frame,page)
				#print ajurl
				#print type(ajurl)
				try:
					page_url = "http://www.meilishuo.com/guang/catalog/dress?nid=210113&cata_id=2001000000000&page=%d"%page
					response = self.opener.open("page_url", timeout=3)
					response = self.opener.open("http://www.meilishuo.com/aj/fullalert/dialog?time_type=1", timeout=3)
					response = self.opener.open("http://www.meilishuo.com/aj/getMsg/", timeout=3)
				except:
					pass
				print  123
				try:
					response = self.opener.open(ajurl, timeout=5)
				except:
					print "except, sleep 1"
					try:	
						try:
							page_url = "http://www.meilishuo.com/guang/catalog/dress?nid=210113&cata_id=2001000000000&page=%d"%page
							response = self.opener.open("page_url", timeout=3)
							response = self.opener.open("http://www.meilishuo.com/guang/catalog/dress?nid=210113&cata_id=2001000000000&frm=daeh", timeout=3)
						except:
							pass
						response = self.opener.open(ajurl, timeout=5)
					except:

						print "continue"
						self.shangyi_fail_pages.append(ajurl)
						continue
				read = response.read()
				items = re.findall("\"url\"\:\"\\\/share\\\/item\\\/[0-9]+\?", read)
				for item in items:
					item = item.replace("\\","")
					goods_url = self.url + item.split(":\"")[1].strip()
					#print item
					#print goods_url	
					self.shangyi_pages.add(goods_url)
				self.get_goods_info()
		
		fail_url = 0
		for ajurl in self.shangyi_fail_pages:
			try:
				response = self.opener.open("http://www.meilishuo.com/guang/catalog/dress?nid=210113&cata_id=2001000000000&frm=daeh", timeout=3)
				response = self.opener.open("http://www.meilishuo.com/aj/fullalert/dialog?time_type=1", timeout=3)
			except:
				pass
			try:
				response = self.opener.open(ajurl, timeout=5)
			except:
				fail_url  = fail_url+1
				print ajurl
				print "fail url %d"%fail_url
				continue
 			read = response.read()
			items = re.findall("\"url\"\:\"\\\/share\\\/item\\\/[0-9]+\?", read)
			for item in items:
				item = item.replace("\\","")
				goods_url = self.url + item.split(":\"")[1].strip()
				#print item
				#print goods_url	
				self.shangyi_pages.add(goods_url)
			self.get_goods_info()
			
		
		print len(self.shangyi_fail_pages)	


	def get_goods_detail(self, url):
		try:
			response = self.opener.open(url)
			read = response.read()
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
			
			####get goods_id
			goods_id = goods.attrs["data-tid"]
			
			####get link
			goods_link = url
			
			####get kind, shangyi = 1
			goods_kind = 1

			####get sub type
			goods_type = 1
			
			import datetime
			goods_time = time.strftime('%Y-%m-%d %H:%M:%S')

			

			#####goods_xiaoliang:
			goods_xiaoliang = 0
			for ele in goods.find_all("li"):
				if u"销量" in ele.text:
					if ele.span is not None:
						jianshu = ele.span.text.strip()
						goods_xiaoliang = re.findall("[0-9]+",jianshu)[0] 
						goods_xiaoliang = int(goods_xiaoliang)
				if u"好评" in ele.text:
					if ele.span is not None:
						pinglun = ele.span.text.strip()
						#print pinglun
						goods_pinglun = re.findall("[0-9]+",pinglun)[0]
						goods_pinglun = int(goods_pinglun)
				if u"喜欢" in ele.text:
					if ele.span is not None:
						xihuan = ele.span.text.strip()
						goods_xihuan = re.findall("[0-9]+",xihuan)[0]
						goods_xihuan = int(goods_xihuan)
			
			self.mydb.cursor.execute("select * from link_info where link = %s", (goods_link,))
			result = self.mydb.cursor.fetchall()
			if(len(result) == 0):
				self.mydb.cursor.execute( "insert into link_info(link, id, name, kind, type, date) values( %s, %s, %s, %s, %s, %s)",(goods_link,goods_id,goods_name,goods_kind,goods_type,goods_time))
			else:
				pass
			self.mydb.cursor.execute("insert into statistic(id, xiaoliang, pinglun, time, xihuan) values(%s, %s, %s, %s, %s)",(goods_id, goods_xiaoliang, goods_pinglun, goods_time, goods_xihuan))
		except:
			print url
			print "error"
	
			
	def get_goods_info(self):
		print len( self.shangyi_pages)
		for url in self.shangyi_pages:
			#print url
			try:
				response = self.opener.open(url)
			except:
				continue
			read = response.read()
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
			except:
				continue
			
			####get link
			goods_link = url
			
			####get kind, shangyi = 1
			goods_kind = 1

			####get sub type
			goods_type = 1
			
			import datetime
			goods_time = time.strftime('%Y-%m-%d %H:%M:%S')

			

			#####goods_xiaoliang:
			goods_xiaoliang = 0
			for ele in goods.find_all("li"):
				if u"销量" in ele.text:
					if ele.span is not None:
						jianshu = ele.span.text.strip()
						goods_xiaoliang = re.findall("[0-9]+",jianshu)[0] 
						goods_xiaoliang = int(goods_xiaoliang)
				if u"好评" in ele.text:
					if ele.span is not None:
						pinglun = ele.span.text.strip()
						print pinglun
						goods_pinglun = re.findall("\([0-9]+",pinglun)[0].split("(")[1]
						goods_pinglun = int(goods_pinglun)
				if u"喜欢" in ele.text:
					if ele.span is not None:
						xihuan = ele.span.text.strip()
						goods_xihuan = re.findall("[0-9]+",xihuan)[0]
						goods_xihuan = int(goods_xihuan)
			
			self.mydb.cursor.execute("select * from link_info where link = %s", (goods_link,))
			result = self.mydb.cursor.fetchall()
			if(len(result) == 0):
				self.mydb.cursor.execute( "insert into link_info(link, id, name, kind, type, date) values( %s, %s, %s, %s, %s, %s)",(goods_link,goods_id,goods_name,goods_kind,goods_type,goods_time))
			else:
				pass
			self.mydb.cursor.execute("insert into statistic(id, xiaoliang, pinglun, time, xihuan) values(%s, %s, %s, %s, %s)",(goods_id, goods_xiaoliang, goods_pinglun, goods_time, goods_xihuan))
		self.shangyi_pages = set()


	
	def get_goods_url(self):
		self.mydb.cursor.execute("select link from link_info")
		result = self.mydb.cursor.fetchall()
		for row in result:
			self.shangyi_pages.add(row[0])	
		print len(self.shangyi_pages)
	def run(self):
		#self.get_main_page()
		#self.get_shangyi_link()
		#self.get_frm_shangyi_page()
		#self.get_aj_shangyi_page()
		self.get_goods_url()
		self.get_shangyi_page()
		self.get_goods_info()	
			
if __name__ == "__main__":
	mls = MlsData("www.meilishuo.com")
	while True:
		mls.run() 			
		time.sleep(3600)
