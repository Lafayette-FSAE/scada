import sys, os

scada_path = '/home/pi/scada-nogit'

sys.path.append(scada_path)
sys.path.append(f'{scada_path}/calibration')

import config
import redis

import utils
import calibration_utils
from calibration import user_cal

import time
import datetime

# import logging as log
# logfile = os.environ['SCADA_LOG']
# log.basicConfig(
# 	level=log.DEBUG,
# 	filename=logfile,
# 	filemode='w',
# 	format='data_calibrator: %(levelname)s - %(message)s - %(asctime)s'
# )

data = redis.Redis(host='localhost', port=6379, db=0)

p = data.pubsub()
p.subscribe('new_data')

def update():

	for target in calibration_utils.targets():
		err, result = calibration_utils.process(target)

		if err:
			print(f'failed to calibrate "{target}", cal_function failed with message: "{err}"')
			# log.warning(f'failed to calibrate "{target}", cal_function failed with message: "{err}"')
		else:
			if type(result) in [float, int]:
				result = round(result, 2)

			data.setex(f"SCADA: {target}", 10, result)

while True:
	if p.get_message():
		update()
	
	time.sleep(0.1)