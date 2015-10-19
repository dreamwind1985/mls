#!/usr/bin/python
# -*- coding: UTF-8 -*-

import MySQLdb

class MyDb():
	def __init__(self,ip,user,passwd,dbname):
		self.db = MySQLdb.connect(ip,user,passwd,dbname,charset="utf8")
		self.cursor = self.db.cursor()
	def close(self):
		self.db.close()	


if __name__ == "__main__":
	sql = "select * from statistic"
	db = MyDb(ip="127.0.0.1", user = "root", passwd="liliang", dbname="mls")
	db.execute(sql) 
	db.close()
