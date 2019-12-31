import config

import can
import can_utils
from can_utils import messages

import calibration_utils
import user_cal

bus = can_utils.bus(config.get('bus_info'))

"""
Reads Data from the CAN bus and performs basic processing
to calibrate it and convert it to to other forms.

Writes processed data back to CAN bus as a PDO

"""

pdo_structure = config.get('process_data')['SCADA']

def update():
	"""
	Runs periodically,

	currently called whenever a sync packet is received,
	but this behavior could be changed

	"""

	for target in calibration_utils.targets():
		err, result = calibration_utils.process(target)
		if err:
			print("Error: {}".format(err))
			break

		can_utils.data_cache.set('SCADA', target, result)

def generate_pdo():
	output = []

	for key in pdo_structure:
		try:
			value = can_utils.data_cache.get_avg('SCADA', key)
			output.append(value)
		except:
			output.append(0x00)

	message = messages.pdo(4, output)
	return message

class Listener(can.Listener):
	def __init__(self, node_id):
		self.node_id = node_id

	def on_message_received(self, msg):

		function, node_id = messages.get_info(msg)

		if function == 'SYNC':
			update()
			pdo = generate_pdo()

			bus.send(pdo)

		if function == 'PDO':

			try:
				node = config.get('can_nodes')[node_id]
			except:
				return

			pdo_structure = config.get('process_data')[node]

			for index, byte in enumerate(msg.data, start=0):
				try:
					can_utils.data_cache.set(node, pdo_structure[index], byte)

				except:
					print('data procecessor: error writing to cache')
					pass



