import sys
import can
import yaml

import can_messages

import can_utils

config = {}

# read config from config.yaml file
with open("config.yaml", 'r') as stream:
	try:
		config = yaml.safe_load(stream)
	except yaml.YAMLError as exc:
		print(exc)


bus = can.interface.Bus(bustype='socketcan', channel='vcan0', bitrate='125000')
notifier = can.Notifier(bus, [])

if(config['emulate_nodes']):

	# append emulators directory to include path
	sys.path.append('emulators')

	# check which emulators are enabled
	if(config['emulate_tsi']):
		import tsi_emulator

		tsi = tsi_emulator.Listener(node_id=3)
		notifier.add_listener(tsi)


	if(config['emulate_packs']):
		import ams_emulator

		pack1 = ams_emulator.Listener(node_id=2)
		notifier.add_listener(pack1)

		pack2 = ams_emulator.Listener(node_id=1)
		notifier.add_listener(pack2)

	if(config['emulate_cockpit']):
		pass

	if(config['emulate_motorcontroller']):
		pass


# modules
sys.path.append('modules')
sys.path.append('calibration')

import data_processor
processor = data_processor.Listener(node_id=4)

notifier.add_listener(processor)

sync = can.Message(arbitration_id=0x80, data=0x00)
sync.is_extended_id = False

# pack_read = can_messages.sdo_read(2, [0x20, 0x12], [0x00])

bus.send_periodic(sync, .1)

for msg in bus:
	pass