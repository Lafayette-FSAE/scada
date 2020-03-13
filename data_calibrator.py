import sys, os

scada_path = os.environ['SCADA_PATH']
sys.path.append(scada_path)

import config
import redis

import utils
import calibration_utils
from calibration import user_cal

import time

data = redis.Redis(host='localhost', port=6379, db=0)

def update():

	for target in calibration_utils.targets():
		err, result = calibration_utils.process(target)

		if err:
			pass # Do logging here
		else:
			data.setex(f"SCADA: {target}", 10, result)

while True:
	update()
	time.sleep(0.1)