import yaml
import logging

# Define class which stores and handles interaction with the SCADA config file
# Everything is static so that no instance have to be passed back and forth
# Use the 'get' method as the main function for accessing the config structure
class Config():
	config = {}
	loaded = False

	# Loads the YAML config file in a config structure
	@staticmethod
	def load():
		if Config.loaded:
			return
		with open("config.yaml", 'r') as stream:
			try:
				Config.config = yaml.safe_load(stream)
				Config.loaded = True
				logging.info('Successfully loaded config file')
			except yaml.YAMLError as exc:
				print(exc)

	# Returns the value associated with the given key in the config structure
	@staticmethod
	def get(key):
		if not Config.loaded:
			Config.load()
		return Config.config[key]

	# Returns a string dump of the entire config structure
	@staticmethod
	def string_dump():
		if not Config.loaded:
			Config.load()
		return yaml.dump(Config.config)