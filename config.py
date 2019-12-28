import yaml
import logging


__config = {}
__loaded = False


# Loads the YAML config file in a config structure
def load():
	global __config, __loaded
	
	if __loaded:
		return
	
	with open('config.yaml', 'r') as stream:
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