import sys
import can
import yaml

import can_utils

import config

bus = can_utils.bus(config.get('bus_info'))
notifier = can.Notifier(bus, [])

if(config.get('emulate_nodes')):

	# append emulators directory to include path
	sys.path.append('emulators')

	# check which emulators are enabled
	if(config.get('emulate_tsi')):
		import tsi_emulator

		tsi = tsi_emulator.Listener(node_id=3)
		notifier.add_listener(tsi)


	if(config.get('emulate_packs')):
		import ams_emulator

		pack1 = ams_emulator.Listener(node_id=2)
		notifier.add_listener(pack1)

		pack2 = ams_emulator.Listener(node_id=1)
		notifier.add_listener(pack2)

	if(config.get('emulate_cockpit')):
		pass

	if(config.get('emulate_motorcontroller')):
		pass


# modules
sys.path.append('modules')
sys.path.append('calibration')

import data_processor
processor = data_processor.Listener(node_id=4)

notifier.add_listener(processor)

sync = can.Message(arbitration_id=0x80, data=0x00)
sync.is_extended_id = False

read = can_utils.messages.sdo_read(node_id=2, index=[0x30, 0x01], subindex=0x02)

master_bus = can_utils.bus(config.get('bus_info'))
master_bus.send_periodic(sync, .1)


import scada_gui
test_value = 10

import can
import can_utils
class Listener(can.Listener):
	def __init__(self, node_id):
		# self.bus = bus
		self.node_id = node_id

	def on_message_received(self, msg):

		global test_value

		function, node_id = can_utils.messages.get_info(msg)

		if function == 'PDO' and node_id == 3:
			pass
			# print(int(msg.data[4]))
			# scada_gui.data[('TSI', 'CURRENT')] = int(msg.data[4])


gui = Listener(node_id=6)
notifier.add_listener(gui)

if __name__ == '__main__':
	scada_gui.main()