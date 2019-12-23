import can
import can_messages
import yaml

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
calibration_functions = {}
processed_data = {}

ams_pdo = config['ams_pdo']
pdo_structure = config['data_processor_pdo']

def init(config):
	pass
# 	ams_pdo = config['ams_pdo']
# 	print(ams_pdo)

def cal_function(target, requires):
	
	def inner(function):
		calibration_functions[target] = (function, requires)
		return function

	return inner


@cal_function(target='PackTemp_Farenheit', requires=['pack1 - ambient_temp'])
def packtemp_farenheit(args):
	temp, *other = args

	return temp * (9/5) + 32

# @cal_function(target='TS Voltage', requires=['pack1 - voltage', 'pack2 - voltage'])
# def net_soc(args):
# 	pack1, pack2, *other = args

# 	return pack1 + pack2

def process(target):
	"""
	Takes a target, looks up the necessary arguments from 
	the bus_data dictionary, and excecutes the associated
	calibration function

	returns a tuple of (error, result)

	"""

	try:
		function, requires = calibration_functions[target]
	except:
		message = "no calibration function defined for target: {}".format(target)
		err = Exception(message)
		return (err, None)

	arguments = []

	for key in requires:

		try:
			argument = bus_data[key]
			arguments.append(argument)
		except:
			message = "could not find key '{}' required for target '{}'".format(key, target)
			# print(message)
			err = Exception(message)
			return (err, None)

	result = function(arguments)

	return (None, result)


def process_all():

	for target in calibration_functions:
		err, result = process(target)
		
		if err:
			print("Error: {}".format(err))
			break

		processed_data[target] = result


class Listener(can.Listener):
	def __init__(self, node_id):
		self.node_id = node_id

	def on_message_received(self, msg):

		function, node_id = can_messages.separate_cob_id(msg.arbitration_id)

		if function == 0x80:
			print(bus_data)
			process_all()

			# Build PDO
			pdo_length = 1
			# pdo_length = object_dictionary['1A03sub0']
			try:
				data = [int(processed_data['PackTemp_Farenheit'])]
			except:
				return

			for key in pdo_structure:
				data.append(processed_data[key])

			print(data)


			message = can_messages.transmit_pdo(self.node_id, data)
			bus.send(message)


		# Deal with TPDOs
		if function == 0x180:

			if node_id == 2: # pack1

				node = 'pack1'

				for index, byte in enumerate(msg.data, start=0):
					key = '{} - {}'.format(node, ams_pdo[index])
					bus_data[key] = byte



