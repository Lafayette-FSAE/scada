import sys
import can
import yaml

import can_messages

config = {}

# read config from config.yaml file
with open("config.yaml", 'r') as stream:
	try:
		config = yaml.safe_load(stream)
	except yaml.YAMLError as exc:
		print(exc)

bus = can.interface.Bus(bustype='socketcan', channel='vcan0', bitrate='125000')
nodes = []

print(config['sdo_data'])

if(config['emulate_nodes']):
	# append emulators directory to include path
	sys.path.append('emulators')

	# check which emulators are enabled
	if(config['emulate_tsi']):
		import tsi_emulator

		tsi = tsi_emulator.Listener(bus, node_id=3)
		nodes.append(tsi)


	if(config['emulate_packs']):
		import ams_emulator

		pack1 = ams_emulator.Listener(bus, node_id=2)
		nodes.append(pack1)

	if(config['emulate_cockpit']):
		pass

	if(config['emulate_motorcontroller']):
		pass


# modules
sys.path.append('modules')
import data_processor

notifier = can.Notifier(bus, nodes)

sync = can.Message(arbitration_id=0x80, data=0x00)
sync.is_extended_id = False

pack_read = can_messages.sdo_read(2, [0x20, 0x12], [0x00])

bus.send_periodic(sync, 1)
# bus.send_periodic(pack_read, 2)


for msg in bus:
	# print(msg)
	pass