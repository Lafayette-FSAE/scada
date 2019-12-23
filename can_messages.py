import can

"""
A collection of useful can messages and helper functions

NOTE: don't forget to set is_extended_id to false on each message

"""

bus = can.interface.Bus(bustype='socketcan', channel='vcan0', bitrate='125000')


def separate_cob_id(cob_id):
	# get last (hex) digit of cob_id
	node_id = cob_id % 16
	function_id = cob_id - node_id

	return (function_id, node_id)


sync = can.Message(arbitration_id=0x80, data=0x00)
sync.is_extended_id = False


def sdo_read(node_id, index, subindex):
	cob_id = 0x600 + node_id
	data = [0x00] + index + subindex + [0x00, 0x00, 0x00, 0x00]

	# print(data)

	# data = [0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00]
	
	message = can.Message(arbitration_id=cob_id, data=data)
	message.is_extended_id = False

	return message

def transmit_pdo(node_id, data):

	"""
	Returns a transmit PDO (Process Data Object) 
	with the given node_id and data


	http://www.byteme.org.uk/canopenparent/canopen/pdo-process-data-objects-canopen/

	"""

	cob_id = 0x180 + node_id

	message = can.Message(arbitration_id=cob_id, data=data)
	message.is_extended_id = False

	return message