
calibration_functions = {}


# Decorator that adds a function to the list of calibration functions
# with the given target and arguments
def cal_function(target, requires):
	
	def inner(function):
		calibration_functions[target] = (function, requires)
		return function

	return inner


def process(target, bus_data):
	"""
	Takes a target, looks up the necessary arguments from 
	the bus_data dictionary, and excecutes the associated
	calibration function

	returns a tuple of (error, result)

	"""

	try:
		function, requires = calibration_functions[target]
	except:
		message = "no calibration function defined for target: {}".format(target)
		err = Exception(message)
		return (err, None)

	arguments = []

	for key in requires:

		try:
			argument = bus_data[key]
			arguments.append(argument)
		except:
			message = "could not find key '{}' required for target '{}'".format(key, target)
			# print(message)
			err = Exception(message)
			return (err, None)

	result = function(arguments)

	return (None, result)


def process_all(targets, data):

	output = {}

	for target in targets:
		err, result = process(target, data)
		
		if err:
			print("Error: {}".format(err))
			break

		output[target] = result

	return output
