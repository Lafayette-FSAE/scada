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

if(config['emulate_nodes']):
	# append emulators directory to include path
	import sys
	sys.path.append('emulators')

	# check which emulators are enabled
	if(config['emulate_tsi']):
		import tsi_emulator as tsi
		
		tsi.init(bustype = config['bustype'])
		tsi.node_id = 3


	if(config['emulate_packs']):
		pass

	if(config['emulate_cockpit']):
		pass

	if(config['emulate_motorcontroller']):
		pass