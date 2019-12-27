import can

FUNCTIONS = {
	# Network Management
	0x000: "NMT",

	# Sync
	0x080: "SYNC",

	# PDOs 1-4
	0x180: 'PDO',
	0x280: 'PDO2',
	0x380: 'PDO3',
	0x480: 'PDO4',

	# SDO Write
	0x580: 'SDO-WRITE',

	# SDO Read
	0x600: 'SDO-READ',
}

def get_function(code):
	return FUNCTIONS.get(code, lambda: None)

def get_code(function):
	inv_functions = {function: code for code, function in FUNCTIONS.items()}

	return hex(inv_functions.get(function))

def can_message(function, node_id, data):
	
	function_code = get_code(function)
	cob_id = function_code + node_id

	message = can.Message(arbitration_id = cob_id, data=data)
	message.is_extended_id = False

	return message

def pdo(node_id, data, pdo_number = 1):
	#http://www.byteme.org.uk/canopenparent/canopen/pdo-process-data-objects-canopen/

	return can_message('PDO', node_id, data)

def sdo_read(node_id, index, subindex=0xFF):
	#http://www.byteme.org.uk/canopenparent/canopen/sdo-service-data-objects-canopen/
	# TODO: use command byte

	command_byte = 0x00 
	data = [command_byte] + index + [subindex] + [0x00, 0x00, 0x00, 0x00]

	return can_message('SDO-READ', node_id, data)

def sdo_write(node_id, index, subindex=0xFF, value=0):
	command_byte = 0x00
	data = [command_byte] + index + [subindex] + [0x00, 0x00, 0x00, hex(value)]

	return can_message('SDO-WRITE', node_id, data)


def get_info(message):
	# get last (hex) digit of cob_id
	node_id = cob_id % 16
	function_id = cob_id - node_id

	function = get_function(function_id)

	return (function, node_id)








