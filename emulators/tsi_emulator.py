import can

def transmit_pdo(node_id, data):
	cob_id = 0x180 + node_id

	message = can.Message(arbitration_id=cob_id, data=data)
	message.is_extended_id = False

	return message


class Listener(can.Listener):
	def __init__(self, bus, node_id):
		self.bus = bus
		self.node_id = node_id

	def on_message_received(self, msg):
		print("TSI message received")
		if msg.arbitration_id == 0x80:
			print("sync")
			#TODO add more PDOs
			#TODO add feature to count syncs before sending PDO
			message = transmit_pdo(node_id=self.node_id, data=[0xFE, 0xDC, 0xBA, 0x98, 0x76, 0x54, 0x32, 0x10])
			self.bus.send(message)
			# Add more CANopen responses here


# sync = can.Message(arbitration_id=0x80, data=0x00)
# bus.send_periodic(sync, 1)

# for msg in bus:
# 	# print(msg)
# 	pass