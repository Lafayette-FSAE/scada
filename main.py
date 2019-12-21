import can
import yaml

config = {}

# read config from config.yaml file
with open("config.yaml", 'r') as stream:
	try:
		config = yaml.safe_load(stream)
	except yaml.YAMLError as exc:
		print(exc)

print(config)

bus = can.interface.Bus(bustype='socketcan', channel='vcan0', bitrate='125000')
nodes = []


if(config['emulate_nodes']):
	# append emulators directory to include path
	import sys
	sys.path.append('emulators')

	# check which emulators are enabled
	if(config['emulate_tsi']):
		import tsi_emulator

		tsi = tsi_emulator.Listener(bus, node_id=3)
		nodes.append(tsi)


	if(config['emulate_packs']):
		pass

	if(config['emulate_cockpit']):
		pass

	if(config['emulate_motorcontroller']):
		pass

notifier = can.Notifier(bus, nodes)

sync = can.Message(arbitration_id=0x80, data=0x00)
sync.is_extended_id = False
bus.send_periodic(sync, 1)

for msg in bus:
	# print(msg)
	pass