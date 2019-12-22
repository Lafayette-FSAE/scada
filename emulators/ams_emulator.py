import can
import can_messages

object_dictionary = {

	# Transmit PDO
	'1A03':		0,
	'1A03sub0':	2, 		# Number of PDO entries
	'1A03sub1':	'2010',	# Entry 1
	'1A03sub2':	'2011', # Entry 2
	'1A03sub3':	'2012', # Entry 3
	'1A03sub4':	0,
	'1A03sub5':	0,
	'1A03sub6':	0,
	'1A03sub7':	0,

	# Temperatures
	'2010': 25, 	# Ambient Temp
	'2011': 30,		# Cell1 Temp
	'2012': 30,		# Cell2 Temp
	'2013': 30,		# Cell3 Temp

	# Error Thresholds
	'2020': 0,		# Cell Temp
	'2020sub0':	0,	# Min Temp
	'2020sub1':	60,	# Max Temp
}


class Listener(can.Listener):
	def __init__(self, bus, node_id):
		self.bus = bus
		self.node_id = node_id

	def on_message_received(self, msg):

		function, node = can_messages.separate_cob_id(msg.arbitration_id)

		# sync
		if function == 0x80:
			# Build PDO
			pdo_length = object_dictionary['1A03sub0']

			data = []

			for i in range(0, pdo_length):
				data_index = object_dictionary['1A03sub{}'.format(i + 1)]
				data.append(object_dictionary[data_index])

			print(data)

			message = can_messages.transmit_pdo(self.node_id, data)
			self.bus.send(message)

		# sdo read
		if function == 0x600 and node == self.node_id:

			command = msg.data[0]
			index = msg.data[1:3]

			index_string = ''.join(format(x, '02x') for x in index)

			value = object_dictionary[index_string]

			print(value)

			
