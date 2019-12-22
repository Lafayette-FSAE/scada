import can
import can_messages

"""
Reads Data from the CAN bus and writes it to a database

"""


class Listener(can.Listener):
	def __init__(self, bus, node_id):
		self.bus = bus
		self.node_id = node_id

	def on_message_received(self, msg):

		function, node = can_messages.separate_cob_id(msg.arbitration_id)

		# Deal with TPDOs
		if function == 0x180:
			pass