#!/usr/bin/python3
import sys, os

scada_path = '/home/fsae/test'

sys.path.append(scada_path)
sys.path.append('{path}/calibrator'.format(path = scada_path))

import config
import redis

import utils
import calibration_utils
import user_cal

import time
import datetime

# import logging as log
# logfile = os.environ['SCADA_LOG']
# log.basicConfig(
#		level=log.DEBUG,
#		filename=logfile,
#		filemode='w',
#		format='data_calibrator: %(levelname)s - %(message)s - %(asctime)s'
# )

data = redis.Redis(host='localhost', port=6379, db=0)

p = data.pubsub()
p.subscribe('bus_data')

def update():

	for target in calibration_utils.targets():
		err, result = calibration_utils.process(target)

		if err:
			pass
			#print(f'failed to calibrate "{target}", cal_function failed with message: "{err}"')
			# log.warning(f'failed to calibrate "{target}", cal_function failed with message: "{err}"')
		else:
			# round numbers to nearest 2 decimal points
			if type(result) in [float, int]:
				result = round(result, 2)

			data.setex("SCADA: {target}".format(target = target), 10, result)

	# let the other processes know that there is new calculated data
	data.publish('calculated_data', '')

while True:
	if p.get_message():
		update()
		
	time.sleep(0.1)
