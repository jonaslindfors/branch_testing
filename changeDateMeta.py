import os
import time
import datetime



p = 'C:/Users/Jonas/Desktop/a/'
dt = datetime.datetime(2017, 4, 22, 12, 00)
convertedTime = time.mktime(dt.timetuple())
myImgs = os.listdir(p)

for file in myImgs:
	path = p + file
	os.utime(path, (convertedTime, convertedTime))