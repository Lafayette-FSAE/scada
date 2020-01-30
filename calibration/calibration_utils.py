from can_utils import data_cache as data

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
			argument = data.get(node, name)
			arguments.append(argument)
		except:
			message = "could not find key '{}' required for target '{}'".format(key, target)
			print(message)
			err = Exception(message)
			return (err, None)

	try:
		result = function(arguments)
	except:
		return (Exception('bad function call, {}'.format(target)), None)

	return (None, result)


# def process_all(targets):

# 	output = {}

# 	for target in targets:
# 		err, result = process(target)
		
# 		if err:
# 			print("Error: {}".format(err))
# 			break

# 		output[target] = result

# 	return output
