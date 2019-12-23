import can
import can_messages


"""
Reads Data from the CAN bus and performs basic processing
to calibrate it and convert it to to other forms.

Writes processed data back to CAN bus as a PDO

"""

bus_data = {}
calibration_functions = {}
ams_pdo = []

def init(config):
	ams_pdo = config['ams_pdo']



processed_data = {
	'PackTemp_Farenheit': 0,
	'Test': 0,
}

def cal_function(target, requires):
	
	def inner(function):
		calibration_functions[target] = (function, requires)
		return function

	return inner


@cal_function(target='PackTemp_Farenheit', requires=['PackTemp'])
def packtemp_farenheit(args):
	temp, *other = args

	return temp * (9/5) + 32

@cal_function(target='Net_State_Of_Charge', requires=['Pack1-SOC', 'Pack2-SOC'])
def net_soc(args):
	pack1, pack2, *other = args

	return pack1 + pack2

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
			print(message)
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

# process_all()



class Listener(can.Listener):
	def __init__(self, bus, node_id):
		self.bus = bus
		self.node_id = node_id

	def on_message_received(self, msg):

		# print("test")

		# function, node = can_messages.separate_cob_id(msg.arbitration_id)

		print(hex(msg.arbitration_id))

		# Deal with TPDOs
		# if function == 0x180:
		# 	print(msg.data)



