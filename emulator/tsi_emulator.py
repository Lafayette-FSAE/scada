#!/usr/bin/python3

import sys, os
import can

import utils
from utils import object_dictionary
from utils import messages

import config

bus = utils.bus(config.get('bus_info'))
notifier = can.Notifier(bus, [])

# Create Object Dictionary
pdo_structure = config.get('process_data')['TSI']

od = object_dictionary.ObjectDictionary()
od.add_keys(pdo_structure)
od.set_pdo_map(pdo_structure)

od.set('state:int', 1)

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

	od.set('current:raw', ramp(time))
	od.set('throttle:raw', ramp(time))
	od.set('state:int', get_state(time))	

	time = time + 1

	od.set('voltage:raw', 100)

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
