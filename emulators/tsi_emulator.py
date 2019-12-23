import can
import can_messages

bus = can.interface.Bus(bustype='socketcan', channel='vcan0', bitrate='125000')


class Listener(can.Listener):
	def __init__(self, bus, node_id):
		self.node_id = node_id

	def on_message_received(self, msg):

		function, node = can_messages.separate_cob_id(msg.arbitration_id)

		# sync
		if function == 0x80:

			data = [0xFE, 0xDC, 0xBA, 0x98, 0x76, 0x54, 0x32, 0x10]

			message = can_messages.transmit_pdo(self.node_id, data)

			# thisbus.send(message)
			bus.send(message)

	# def on_error(self, err):
	# 	print("error")
	# 	print(err)