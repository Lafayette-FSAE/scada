import time

__data = {}

nodes = {
	'TSI': 3,
}


def get(node, key):
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