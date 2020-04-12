#!/usr/bin/python3
import sys, os

lib_path = '/usr/etc/scada'
config_path = '/usr/etc/scada/config'

sys.path.append(lib_path)
sys.path.append(config_path)

import config
import redis

import utils
from utils import calibration
import user_cal

import time
import datetime

# TODO: reintroduce verbose logging

# Configure Redis interface
data = redis.Redis(host='localhost', port=6379, db=0)
p = data.pubsub()
p.subscribe('bus_data')

def execute(cal_function):
	argument_keys = calibration.get_arguments(cal_function)
	arguments = []
	for key in argument_keys:
		value = data.get(key)
		if hasattr(value, 'decode'):
			value = value.decode()
			value = int(value)
			print(key + ' ' + str(value))
		arguments.append(value)
		
	function = calibration.get_function(cal_function)
	result = function(arguments)
	return result
		
def update():
	for cal_function in calibration.get_function_names():
		try:
			result = execute(cal_function)
			data.setex(cal_function, 10, result)	
		except Exception as e: 
			print(e)
			print()
			pass
			#print(f'failed to calibrate "{target}", cal_function failed with message: "{err}"')
			# log.warning(f'failed to calibrate "{target}", cal_function failed with message: "{err}"')

	# let the other processes know that there is new calculated data
	data.publish('calculated_data', '')

while True:
	while p.get_message():
		update()
		
	time.sleep(0.1)
