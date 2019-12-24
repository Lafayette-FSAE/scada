def separate_cob_id(cob_id):
	# get last (hex) digit of cob_id
	node_id = cob_id % 16
	function_id = cob_id - node_id

	return (function_id, node_id)

class ObjectDictionary():

	def __init__(self, property_list):
		self.od = {} 		# the literal object dictionary
							# maps a two byte index and one byte subindex to a value
		
		self.od_map = {}	# maps indeces in the object dictionary to 
							# human readable property names
		
		self.next_index = 0x2000	# user defined properties start here

		for property in property_list:
			self.od_map[property] = self.next_index # add index
			self.od[self.od_map[property]] = 0		# initialize value to 0
			self.next_index += 1					# increment next index


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

	def set_pdo_map(property_list):
		pdo_length = len(property_list)

		for property in property_list:
			index = self.od_map[property]


