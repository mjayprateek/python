""" will move subtitles forward or backward by given
number of milliseconds """

from os import path
from datetime import datetime
from datetime import timedelta
import re
import sys
import shutil
import os

timeDurationRegex = '(\\d{2}:\\d{2}:\\d{2},\\d{3}) --> (\\d{2}:\\d{2}:\\d{2},\\d{3})'

def move(file, direction, millis):
	f = open(file, 'r', encoding = "ISO-8859-1")

	temp_file_path = path.join(path.dirname(file), 'temp_file.srt')
	temp_file = open(temp_file_path, 'wt')

	for line in f:
		print(line)
		m = matches(line, timeDurationRegex)
		
		if(m!=None and len(m.groups()) == 2):
			print('matched')
			start_time = moveTimeBy(m.group(1), millis, direction)
			stop_time = moveTimeBy(m.group(2), millis, direction)

			line = start_time + ' --> ' + stop_time + '\n'

		temp_file.write(line)


	f.close()
	temp_file.close()

	print ("deleting the original file")
	os.remove(file)

	print (" moving file %s to %s " % (temp_file, file))
	os.rename(temp_file_path, file)



def matches(str, regex):
	p = re.compile(regex)
	m = p.match(str)

	return m

def moveTimeBy(date_str, dur_in_millis, direction):
	d = datetime.strptime(date_str, '%H:%M:%S,%f')
	dur = timedelta(microseconds = int(dur_in_millis)*1000)

	print("duration " + str(dur))

	if(direction=='f'):
		d = d + dur
	else:
		d = d - dur
	
	new_time = d.strftime('%H:%M:%S,%f')[0:-3]
	print("old time " + date_str)
	print ("new time " + new_time)

	return new_time


if __name__ == "__main__":
	args = sys.argv

	if(len(args)!=4):
		print ("Error. Total number of arguments: %s Please supply exactly three arguments in the following order: subtitle_file_path, direction_of_shift ('f' or 'b'), time_in_millis"%(len(args)-1))

		sys.exit()

	print ('file path: ' + args[1])
	print ('direction of shift: ' + 'forward' if(args[2]=='f') else 'backward')
	print ('number of milliseconds: ' + args[3])

	print ('shifting subtitles ...' )

	move(args[1], args[2], args[3])
















