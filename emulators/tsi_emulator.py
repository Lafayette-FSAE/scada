import can
import can_messages

class Listener(can.Listener):
	def __init__(self, bus, node_id):
		self.bus = bus
		self.node_id = node_id

	def on_message_received(self, msg):

		function, node = can_messages.separate_cob_id(msg.arbitration_id)

		# sync
		if function == 0x80:
			print("sync")

			data = [0xFE, 0xDC, 0xBA, 0x98, 0x76, 0x54, 0x32, 0x10]

			message = can_messages.transmit_pdo(self.node_id, data)
			self.bus.send(message)
