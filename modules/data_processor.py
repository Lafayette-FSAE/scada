import yaml

import can
import can_utils

from can_utils import messages

import calibration_utils

import config

bus = can.interface.Bus(bustype='socketcan', channel='vcan0', bitrate='125000')

"""
Reads Data from the CAN bus and performs basic processing
to calibrate it and convert it to to other forms.

Writes processed data back to CAN bus as a PDO

"""

import user_cal
import tsi_cal

input_data = {}
output_data = {}
errors = {}

pdo_structure = config.get('data_processor_pdo')

def update():
	"""
	Runs periodically,

	currently called whenever a sync packet is received,
	but this behavior could be changed

	"""

	output_data = calibration_utils.process_all(targets=pdo_structure, data=input_data)

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

		if function == 'PDO':

			try:
				node = config.get('can_nodes')[node_id]
			except:
				return

			if node == 'pack1' or node == 'pack2':
				pdo_structure = config.get('ams_pdo')
			else:
				pdo_structure = config.get('{}_pdo'.format(node))

			for index, byte in enumerate(msg.data, start=0):
				try:
					key = '{} - {}'.format(node, pdo_structure[index])
					input_data[key] = byte
				except:
					pass



