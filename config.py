import os

import yaml
import logging

__config = {}
__loaded = False

try:
	config_path = os.environ['SCADA_CONFIG']
except:
	config_path = '/home/pi/scada-nogit/config.yaml'

# Loads the YAML config file in a config structure
def load():
	global __config, __loaded
	
	if __loaded:
		return
	
	with open(config_path, 'r') as stream:
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