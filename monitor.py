#!/usr/bin/python

import os
import time
import thread

def monitor_report():
	while True:
		date = time.strftime("%H:%M", time.localtime(time.time()))
		hour = date.split(":")[0]
		if int(hour) == 8:
			os.system("/root/work/wangpi/query.py")
		time.sleep(3500)		



thread.start_new_thread(monitor_report,())

while True:
	result = os.popen("ps axu | grep 'mls.py'| grep -v 'grep'").readlines()
	if len(result) == 0:
		os.system("/root/work/wangpi/mls.py &")
	elif len(result) > 1:
		print "killed"
		os.system("killall -9 mls.py ")
	else:
		pass
	
	print 1	
	
	time.sleep(60)
