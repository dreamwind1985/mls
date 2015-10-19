#!/usr/bin/python
#-*- coding: UTF-8 -*-


import mydb

import time
import datetime
import os
def get_today_time():
	date = time.strftime('%y-%m-%d', time.localtime(time.time()))
	date_0 = date + " 00:00:00"	
	date_1 = date + " 23:59:59"
	return (date_0, date_1)
def get_lastday_time():
	date = time.strftime("%y-%m-%d", time.localtime(time.time()-86400))
	date_0 = date + " 00:00:00"
	date_1 = date + " 23:59:59"
	return (date_0, date_1)
class query():
	def __init__(self):
		self.db = mydb.MyDb(ip = "127.0.0.1", user = "root", passwd = "liliang", dbname = "mls")
	def query_day_top(self):
		today = get_today_time()
		lastday = get_lastday_time()
		self.db.cursor.execute("select * from link_info")
		results = self.db.cursor.fetchall()
		self.result = []
		for row in results:
			link = row[0]
			id = row[1]
			name = row[2]
	
			xiaoliang_t = 0
			xihuan_t = 0
			pinglun_t  = 0
			xiaoliang_l = 0
			xihuan_l = 0
			pinglun_l =0
			time_t = row[5]
			time_l = row[5]
		
			xiaoliangcha = 0
			pingluncha = 0
			xihuancha = 0

			self.db.cursor.execute("select * from statistic where id=%s and time between %s and %s",(id, today[0],today[1]))
			rs = self.db.cursor.fetchall()
			if len(rs) > 1:
				max_ts = 9999999999
				for r in rs:
					ta = time.strptime(str(r[3]),"%Y-%m-%d %H:%M:%S")
					ts = int(time.mktime(ta))
					if ts < max_ts:
						max_ts = ts
						xiaoliang_t = r[1]
						pinglun_t = r[2]
						xihuan_t = r[4]
						time_t = r[3]
						
			self.db.cursor.execute("select * from statistic where id=%s and time between %s and %s",(id, lastday[0],lastday[1]))
			rs = self.db.cursor.fetchall()
			if len(rs) > 1:
				max_ls = 9999999999
				for r in rs:
					ta = time.strptime(str(r[3]),"%Y-%m-%d %H:%M:%S")
					ts = int(time.mktime(ta))
					if ts < max_ls:
						max_ls = ts
						xiaoliang_l = r[1]
						pinglun_l = r[2]
						xihuan_l = r[4]
						time_l = r[3]
			xiaoliangcha = int(xiaoliang_t) - int(xiaoliang_l)
			pingluncha = pinglun_t - pinglun_l
			xihuancha = xihuan_t - xihuan_l
			ele = {"link":link, "id":id, "xiaoliang_t":xiaoliang_t, "xihuan_t":xihuan_t,"pinglun_t":pinglun_t, "time_t":time_t, "xiaoliang_l":xiaoliang_l, "xihuan_l":xihuan_l, "pinglun_t":pinglun_t, "time_l":time_l, "xiaoliangcha":xiaoliangcha, "pingluncha":pingluncha, "xihuancha":xihuancha}
			self.result.append(ele)
		xls = sorted(self.result, key = lambda x:x["xiaoliangcha"],reverse = True)
		xhs = sorted(self.result, key = lambda x:x["xihuancha"],reverse = True)
		pls = sorted(self.result, key = lambda x:x["pingluncha"],reverse = True)
		xls_l = []
		print xls
		for i in range(0,100):
			 xls_l.append(xls[i])
		self.save_to_file(xls_l)
		self.save_to_html(xls_l)
	
	def save_to_file(self, di):
		fname ="/root/work/wangpi/report/"+str(int(time.time()))
		f = open(fname , "w")
		title = "链接\t\t\t\t\t\t前一天总销量\t当天总销量\t一天销量\n"
		f.write(title)
		for ele in di:
			line = "%s\t%d\t\t\t%d\t\t\t%d\t\t\t%d\n"%(ele["link"],int(ele["xiaoliang_l"]),int(ele["xiaoliang_t"]),int(ele["xiaoliangcha"]),int(ele["pinglun_t"]))
			f.write(line)


		f.close()


	def save_to_html(self,di):
		date = time.strftime('%Y-%m-%d', time.localtime(time.time()))
		fname = "/root/work/wangpi/report/"+date
		f = open(fname,"w")
		begin = '<h1>%s</h1><table border="1"><tr><th>链接</th><th>前一天总销量\t</th><th>当天总销量\t</th><th>一天销量</th></th><th>评论数</th></tr>'%date
		f.write(begin)
		for ele in di:
			link = "<a href='%s'>%s</a>"%(ele["link"],ele["link"])
			line="<tr><td>%s</td><td>%d</td><td>%d</td><td>%d</td><td>%d</td></tr>"%(link,ele["xiaoliang_l"],ele["xiaoliang_t"],ele["xiaoliangcha"],ele["pinglun_t"])
			f.write(line)
		f.write("</table>")
		f.close()
		
		d_dir = "/usr/local/nginx/html/mls_report"
		os.system("cp -f %s %s"%(fname,d_dir))
		
if __name__ =="__main__":
	q = query()
	q.query_day_top()	
	
		 
		
			
		
