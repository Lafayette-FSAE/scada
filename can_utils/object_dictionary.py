import can
import yaml

def parse_eds_yaml(path):
	output = {}

	with open(path, 'r') as stream:
		try:
			output = yaml.safe_load(stream)
			Config.loaded = True
		except yaml.YAMLError as exc:
			print(exc)


	return output


class ObjectDictionary():

	def __init__(self, eds_path, eds_yaml_path):
		self.od = {} 		# the literal object dictionary
							# maps a two byte index and one byte subindex to a value
		
		self.od_map = {}	# maps indeces in the object dictionary to 
							# human readable property names
		
		self.next_index = 0x2000	# user defined properties start here




	def __str__(self):
		output = ''

		for key in self.od_map:
			line = 'Name: {} \t Value: {} \t Index: {} \n'.format(
				key, self.od[self.od_map[key]], hex(self.od_map[key]))
			
			output = output + line
		
		return output

	def get(key):
		return self.od[self.od_map[key]]

	def set(key, value):
		self.od[self.od_map[key]] = value

	def set_pdo_map(property_list, pdo_number=1):
		pdo_length = len(property_list)

		for property in property_list:
			index = self.od_map[property]