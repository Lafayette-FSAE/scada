import config
import redis

import sys
sys.path.append('calibration')

import calibration_utils
import user_cal

import time

data = redis.Redis(host='localhost', port=6379, db=0)

def update():

	for target in calibration_utils.targets():
		err, result = calibration_utils.process(target)

		if err:
			pass # Do logging here
		else:
			data.set(f"SCADA: {target}", result)

while True:
	update()
	time.sleep(0.1)