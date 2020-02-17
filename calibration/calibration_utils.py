from can_utils import data_cache as data

import redis
data_redis = redis.Redis(host='localhost', port=6379, db=0)

__calibration_functions = {}

# Decorator that adds a function to the list of calibration functions
# with the given target and arguments
def cal_function(target, requires):

	def inner(function):
		__calibration_functions[target] = (function, requires)
		return function

	return inner

def targets():
	return list(__calibration_functions.keys())

def process(target):
	"""
	Takes a target, looks up the necessary arguments from 
	the bus_data dictionary, and excecutes the associated
	calibration function

	returns a tuple of (error, result)

	"""

	try:
		function, requires = __calibration_functions[target]
	except:
		message = "no calibration function defined for target: {}".format(target)
		err = Exception(message)
		return (err, None)

	arguments = []

	for key in requires:

		if type(key) == str:
			node, name = key.split(': ', 1)

		else:
			node, name = key

		try:
			argument_raw = data_redis.get(f"{node}: {name}")
			argument = int(argument_raw)
			arguments.append(argument)
		except:
			message = "could not find key '{}' required for target '{}'".format(key, target)
			err = Exception(message)
			return (err, None)

	try:
		result = function(arguments)
	except Exception as error:
		return (error, None)
		# pass
		# return (Exception('Error in cal_function: {} \n {}'.format(target, err)), None)

	return (None, result)