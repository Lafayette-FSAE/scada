#!/usr/bin/python3

import sys, os

sys.path.append('/home/fsae/test')
import can

import can_utils

from can_utils import object_dictionary
from can_utils import messages

import config

bus = can_utils.bus(config.get('bus_info'))
notifier = can.Notifier(bus, [])

# Create Object Dictionary
pdo_structure = config.get('process_data')['TSI']

od = object_dictionary.ObjectDictionary()
od.add_keys(pdo_structure)
od.set_pdo_map(pdo_structure)

od.set('STATE', 1)

maxval = 255
def ramp(t):
	return t % maxval

def get_state(t):
	if t < 20:
		return 1 
	elif t < 40:
		return 2
	elif t < 45:
		return 3
	elif t < 50:
		return 4
	else:
		return 5

time = 0
def update():
	global time

	od.set('TS_CURRENT', ramp(time))
	od.set('THROTTLE', ramp(time))
	od.set('STATE', get_state(time))	

	time = time + 1

	od.set('TS_VOLTAGE', 100)

class Listener(can.Listener):
	def __init__(self, node_id):
		self.node_id = node_id

	def on_message_received(self, msg):

		function, node = messages.get_info(msg)

		if function == 'SYNC':

			# Send Process Data
			data = od.get_pdo_data()
			message = messages.pdo(self.node_id, data)
			bus.send(message)
