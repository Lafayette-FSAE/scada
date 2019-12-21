import can

bus = {}
node_id = 0

def init(bustype = 'virtual'):
	if bustype == 'virtual':
		bus = can.interface.Bus(bustype='socketcan', channel='vcan0', bitrate='125000')

def transmit_pdo(node_id, data):
	cob_id = 0x180 + node_id

	message = can.Message(arbitration_id=cob_id, data=data)
	message.is_extended_id = False

	return message


message = transmit_pdo(node_id=3, data=[0xFE, 0xDC, 0xBA, 0x98, 0x76, 0x54, 0x32, 0x10])
