import subprocess
from time import sleep
import datetime

while True:
	subprocess.Popen(['python3', 'asursoChecker.py'])

	sleep(3)

	print('===========')
	print(datetime.datetime.now())
	print('===========')
	
	sleep(60*3)