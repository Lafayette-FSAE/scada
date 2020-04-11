#!/usr/bin/python3
import sys, os

scada_path = '/home/fsae/scada'

sys.path.append(scada_path)
sys.path.append('{path}/calibrator'.format(path = scada_path))

import config
import redis

import utils
import calibration_utils
import user_cal

import time
import datetime

# TODO: reintroduce verbose logging

# Configure Redis interface
data = redis.Redis(host='localhost', port=6379, db=0)
p = data.pubsub()
p.subscribe('bus_data')

def execute(cal_function):
	argument_keys = calibration_utils.get_arguments(cal_function)
	arguments = []
	for key in argument_keys:
		value = int(data_redis.get(key))
		arguments.append(value_int)
		
	function = calibration_utils.get_function(cal_function)
	result = function(arguments)
	return result
		
def update():

	for cal_function in calibration_utils.get_function_names():
		try:
			result = execute(cal_function)
			data.setex(cal_function, 10, result)	
		except: 
			print(f'failed to calibrate "{target}", cal_function failed with message: "{err}"')
			# log.warning(f'failed to calibrate "{target}", cal_function failed with message: "{err}"')

	# let the other processes know that there is new calculated data
	data.publish('calculated_data', '')

while True:
	while p.get_message():
		update()
		
	time.sleep(0.1)