import yaml

import can
import can_utils
import can_messages

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

import user_cal
import tsi_cal

bus_data = {}
processed_data = {}

pdo_structure = config['data_processor_pdo']

def update():
	"""
	Runs periodically,

	currently called whenever a sync packet is received,
	but this behavior could be changed

	"""

	processed_data = calibration_utils.process_all(targets=pdo_structure, data=bus_data)

	data = []

	for key in pdo_structure:
		try:
			data.append(int(processed_data[key]))
		except:
			data.append(0x00)

	message = can_messages.transmit_pdo(4, data)
	bus.send(message)



class Listener(can.Listener):
	def __init__(self, node_id):
		self.node_id = node_id

	def on_message_received(self, msg):

		function, node_id = can_utils.separate_cob_id(msg.arbitration_id)

		if function == 0x80:
			update()


		# Deal with TPDOs
		if function == 0x180:

			try:
				node = config['can_nodes'][node_id]
			except:
				return

			if node == 'pack1' or node == 'pack2':
				pdo_structure = config['ams_pdo']
			else:
				pdo_structure = config['{}_pdo'.format(node)]

			for index, byte in enumerate(msg.data, start=0):
				try:
					key = '{} - {}'.format(node, pdo_structure[index])
					bus_data[key] = byte
				except:
					pass



