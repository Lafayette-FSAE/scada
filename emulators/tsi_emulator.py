import can

from can_utils import object_dictionary
from can_utils import messages

od = object_dictionary.ObjectDictionary()

# TODO: needs cleaner import syntax

bus = can.interface.Bus(bustype='socketcan', channel='vcan0', bitrate='125000')

od.add_key('TS_VOLTAGE')
od.add_key('TS_CURRENT')
od.add_key('TEMP1')
od.add_key('TEMP2')
od.add_key('FLOW_RATE')

od.set_pdo_map(['TS_VOLTAGE', 'TS_CURRENT', 'TEMP1', 'TEMP2', 'FLOW_RATE'])

maxval = 100
def ramp(t):
	return t % maxval

time = 0
print(time)

def update():
	global time

	print(time)
	od.set('TS_CURRENT', ramp(time))
	time = time + 1

class Listener(can.Listener):
	def __init__(self, node_id):
		self.node_id = node_id

	def on_message_received(self, msg):

		function, node = messages.get_info(msg)

		# sync
		if function == 'SYNC':

			update()
			data = od.get_pdo_data()
			message = messages.pdo(self.node_id, data)
			bus.send(message)