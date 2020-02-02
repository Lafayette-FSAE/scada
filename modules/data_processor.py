import config

import can
import can_utils
from can_utils import messages

import calibration_utils

import user_cal

import database_utils as db_utils

db_utils.add_node('tsi', config.get('process_data').get('TSI'))
db_utils.add_node('pack1', config.get('process_data').get('PACK1'))
db_utils.add_node('pack2', config.get('process_data').get('PACK2'))
db_utils.add_node('scada', config.get('process_data').get('SCADA'))
db_utils.add_node('motor', config.get('process_data').get('MOTOR'))

bus = can_utils.bus(config.get('bus_info'))

"""
Reads Data from the CAN bus and performs basic processing
to calibrate it and convert it to to other forms.

Writes processed data back to CAN bus as a PDO

"""

pdo_structure = config.get('process_data').get('SCADA')

def update():
	"""
	Runs periodically,

	currently called whenever a sync packet is received,
	but this behavior could be changed

	"""

	for target in calibration_utils.targets():
		err, result = calibration_utils.process(target)
		if err:
			# print("Error: {}".format(err))
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

		if msg.arbitration_id == 0x555:
			function, node_id = ('PDO-1', 3)
		else:
			function, node_id = messages.get_info(msg)

		if function == 'SYNC':
			update()
			
			pdo = generate_pdo()
			bus.send(pdo)

		if function in ['PDO-1', 'PDO-2', 'PDO-3', 'PDO-4']:

			_, pdo_number = function.split('-')

			try:
				node = config.get('can_nodes').get(node_id)
			except:
				return

			# append pdo number to node name to distinguish different
			# pdo mappings
			if pdo_number == '1':
				pdo_structure = config.get('process_data').get(node)
			else:
				pdo_structure = config.get('process_data').get('{}-{}'.format(node, pdo_number))
			

			db_utils.log_pdo(node, msg.data)
			for index, byte in enumerate(msg.data, start=0):
				# try:
				can_utils.data_cache.set(node, pdo_structure[index], byte)

				# except:
					# print('data procecessor: error writing to cache')
					# pass


