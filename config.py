import yaml

class Config():
	config = {}
	loaded = False

	@staticmethod
	def load():
		if Config.loaded:
			return
		with open("config.yaml", 'r') as stream:
			try:
				Config.config = yaml.safe_load(stream)
				Config.loaded = True
				print('Loaded config')
			except yaml.YAMLError as exc:
				print(exc)

	@staticmethod
	def get(key):
		if not Config.loaded:
			Config.load()
		return Config.config[key]

	@staticmethod
	def string_dump():
		if not Config.loaded:
			Config.load()
		return yaml.dump(Config.config)