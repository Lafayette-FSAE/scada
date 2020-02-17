import sys, os

scada_path = os.environ['SCADA_PATH']
sys.path.append(scada_path)

import config
import redis
import can
import utils
from utils import messages

# open a connection to the redis server where we will
# be writing data
data = redis.Redis(host='localhost', port=6379, db=0)

class Listener(can.Listener):
	def on_message_received(self, msg):

		# infer the CANOpen protocol used and node id of sender
		protocol, node_id = messages.get_info(msg)

		# if the protocol used is one of the four types
		# of PDOs (Process Data Objects), then log it
		if protocol in ['PDO-1', 'PDO-2', 'PDO-3', 'PDO-4']:

			_, pdo_number = protocol.split('-')

			# check the config file to find out name of node
			try:
				node = config.get('can_nodes').get(node_id)
			except:
				return

			# check the config file to figure out expected
			# structure of the process data
			if pdo_number == '1':
				pdo_structure = config.get('process_data').get(node)
			else:
				pdo_structure = config.get('process_data').get('{}-{}'.format(node, pdo_number))

			# separate can message into bytes and write each one
			# to the redis server with its name as defined in the
			# config file

			pipe = data.pipeline()

			for index, byte in enumerate(msg.data, start=0):
				# try:
				pipe.setex(f"{node}: {pdo_structure[index]}", 10, byte)

			pipe.execute()
			data.publish('new_data', '')

if __name__ == "__main__":
	bus = utils.bus(config.get('bus_info'))
	notifier = can.Notifier(bus, [])
	notifier.add_listener(Listener())

	for msg in bus:
		pass