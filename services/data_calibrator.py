import sys, os

scada_path = os.environ['SCADA_PATH']
sys.path.append(scada_path)
sys.path.append(f'{scada_path}/calibration')

import config
import redis

import utils
import calibration_utils
from calibration import user_cal

import time

data = redis.Redis(host='localhost', port=6379, db=0)

p = data.pubsub()
p.subscribe('new_data')

def update():

	for target in calibration_utils.targets():
		err, result = calibration_utils.process(target)

		if err:
			pass # Do logging here
		else:
			if type(result) in [float, int]:
				result = round(result, 2)

			data.setex(f"SCADA: {target}", 10, result)

while True:
	if p.get_message():
		update()
	
	time.sleep(0.5)