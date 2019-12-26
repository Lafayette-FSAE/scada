import can

def sdo_read(node_id, index, subindex):
	cob_id = 0x600 + node_id
	data = [0x00] + index + subindex + [0x00, 0x00, 0x00, 0x00]
	
	message = can.Message(arbitration_id=cob_id, data=data)
	message.is_extended_id = False

	return message

def sdo_write(node_id, index, subindex, value):
	pass

def transmit_pdo(node_id, data, pdo_number = 1):

	"""
	Returns a transmit PDO (Process Data Object) 
	with the given node_id and data


	http://www.byteme.org.uk/canopenparent/canopen/pdo-process-data-objects-canopen/

	"""

	function_id = hex( (pdo_number * 16 * 16) + (8 * 16))

	print(transmit_pdo)

	cob_id = function_id + node_id

	message = can.Message(arbitration_id=cob_id, data=data)
	message.is_extended_id = False

	return message