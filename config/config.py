import os, sys

import yaml
import logging

__config = {}
__loaded = False

lib_path = '/usr/etc/scada'
config_path = '/usr/etc/scada/config'

sys.path.append(lib_path)
sys.path.append(config_path)

# Loads the YAML config file in a config structure
def load():
	global __config, __loaded
	
	if __loaded:
		return
	
	with open(config_path + '/config.yaml', 'r') as stream:
	# with open(os.eniron[])
		try:
			__config = yaml.safe_load(stream)
			__loaded = True
			logging.info('Successfully loaded config file')
		except yaml.YAMLError as exc:
			print(exc)


# Returns the value associated with the given key in the config structure
def get(key):
	global __config, __loaded
	
	if not __loaded:
		load()
	
	return __config[key]


# Returns a string dump of the entire config structure
def string_dump():
	global __config, __loaded
	
	if not __loaded:
		load()
	
	return yaml.dump(__config)
