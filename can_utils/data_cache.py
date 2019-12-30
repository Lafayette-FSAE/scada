import time

__data = {}

def get(node, key=None):

	if key == None:
		if type(node) == str:
			node, key = node.split(': ', 1)
			# print(node)
			# print(key)
			# print(__data[(node, key)])
			# print('{}, {}, {}'.format(node, key, __data[(node, key)]))

	try:
		value, timestamp = __data[(node, key)]
		return value
	except:
		pass

def set(node, key, value):
	__data[(node, key)] = (value, time.time())

def get_keys():
	return list(__data.keys())

def track_data(node, object_dictionary):
	pass