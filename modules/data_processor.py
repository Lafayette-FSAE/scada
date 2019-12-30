import yaml

import can
import can_utils

from can_utils import messages

import calibration_utils

import config

bus = can_utils.bus(config.get('bus_info'))

"""
Reads Data from the CAN bus and performs basic processing
to calibrate it and convert it to to other forms.

Writes processed data back to CAN bus as a PDO

"""

import user_cal
import tsi_cal

# input_data = {}
output_data = {}
errors = {}

pdo_structure = config.get('data_processor_pdo')

def update():
	"""
	Runs periodically,

	currently called whenever a sync packet is received,
	but this behavior could be changed

	"""

	# output_data = calibration_utils.process_all(targets=pdo_structure)


	for target in calibration_utils.targets():
		err, result = calibration_utils.process(target)
		
		if err:
			print("Error: {}".format(err))
			break

		can_utils.data_cache.set('SCADA', target, result)



	data = []

	for key in pdo_structure:
		try:
			data.append(int(output_data[key]))
		except:
			data.append(0x00)

	message = messages.pdo(4, data)
	bus.send(message)



class Listener(can.Listener):
	def __init__(self, node_id):
		self.node_id = node_id

	def on_message_received(self, msg):

		function, node_id = messages.get_info(msg)

		if function == 'SYNC':
			update()
			pass

		if function == 'PDO':

			try:
				node = config.get('can_nodes')[node_id]
			except:
				return

			pdo_structure = config.get('{}_pdo'.format(node))

			for index, byte in enumerate(msg.data, start=0):
				try:
					can_utils.data_cache.set(node, pdo_structure[index], byte)

				except:
					print('data procecessor: error writing to cache')
					pass



