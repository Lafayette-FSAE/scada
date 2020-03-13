import time
import collections

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

# def get_avg(target):
# 	node, key = target.split(': ', 1)
# 	result = 0
# 	d = __data[(node, key)]
# 	for value in d:
# 		result = result + value
# 	result = result / len(d)
# 	return result

def set(node, key, value):
	# print()
	# print(node)
	# print(key)
	# print(value)
	# print()

	# if not (node, key) in __data:
	# 	__data[(node, key)] = collections.deque(maxlen=10)
	# __data[(node, key)].append(value)
	__data[(node, key)] = (value, time.time())

def get_keys():
	return list(__data.keys())

def track_data(node, object_dictionary):
	pass