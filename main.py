import sys
import can
import yaml

import can_utils

import config

bus = can_utils.get_bus(config.get('bus_info')['bustype'])
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

bus.send_periodic(read, 1)
bus.send_periodic(sync, .1)

for msg in bus:
	pass