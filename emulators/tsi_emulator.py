import can

import can_utils

from can_utils import object_dictionary
from can_utils import messages

import config

bus = can_utils.bus(config.get('bus_info'))

# Create Object Dictionary
pdo_structure = config.get('process_data')['TSI']

od = object_dictionary.ObjectDictionary()
od.add_keys(pdo_structure)
od.set_pdo_map(pdo_structure)

maxval = 100
def ramp(t):
	return t % maxval

time = 0
def update():
	global time

	od.set('TS_CURRENT', ramp(time))
	time = time + 1

	od.set('TS_VOLTAGE', 100)

class Listener(can.Listener):
	def __init__(self, node_id):
		self.node_id = node_id

	def on_message_received(self, msg):

		function, node = messages.get_info(msg)

		if function == 'SYNC':

			update()

			# Send Process Data
			data = od.get_pdo_data()
			message = messages.pdo(self.node_id, data)
			bus.send(message)