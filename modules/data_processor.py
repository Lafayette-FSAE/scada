import can
import can_messages
import yaml

import calibration_utils

bus = can.interface.Bus(bustype='socketcan', channel='vcan0', bitrate='125000')

"""
Reads Data from the CAN bus and performs basic processing
to calibrate it and convert it to to other forms.

Writes processed data back to CAN bus as a PDO

"""

config = {}

# read config from config.yaml file
with open("config.yaml", 'r') as stream:
	try:
		config = yaml.safe_load(stream)
	except yaml.YAMLError as exc:
		print(exc)


bus_data = {}
processed_data = {}

ams_pdo = config['ams_pdo']
pdo_structure = config['data_processor_pdo']


class Listener(can.Listener):
	def __init__(self, node_id):
		self.node_id = node_id

	def on_message_received(self, msg):

		function, node_id = can_messages.separate_cob_id(msg.arbitration_id)

		if function == 0x80:
			processed_data = calibration_utils.process_all(bus_data)

			data = []

			for key in pdo_structure:
				try:
					data.append(int(processed_data[key]))
				except:
					data.append(0x00)

			message = can_messages.transmit_pdo(self.node_id, data)
			bus.send(message)


		# Deal with TPDOs
		if function == 0x180:

			if node_id == 2: # pack1

				node = 'pack1'

				for index, byte in enumerate(msg.data, start=0):
					key = '{} - {}'.format(node, ams_pdo[index])
					bus_data[key] = byte

			if node_id == 1: # pack2

				node = 'pack2'

				for index, byte in enumerate(msg.data, start=0):
					key = '{} - {}'.format(node, ams_pdo[index])
					bus_data[key] = byte



