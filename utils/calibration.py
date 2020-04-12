
""" 
A dictionary containing a list of all calibration functions. functions are
indexed by the name of their output, eg: "pack1:voltage" for the voltage
measured by pack1 and are stored as a tuple of the function itself, and a 
list of the names of its arguments.

Output strings and argument strings both represent keys in the redis database

For example, a calibration function for calculating power from the tsi 
current and voltage would be stored as:

__calibration_functions['tsi:power'] = (<function>, ["tsi:voltage", "tsi:current"])
"""
__calibration_functions = {}

# Decorator that adds a function to the list of calibration functions
# with the given output and arguments
def cal_function(output, arguments):
	def inner(function):
		__calibration_functions[output] = (function, arguments)
		return function

	return inner

""" Helper Functions for pulling data from __calibration_functions"""

def get_function_names():
	return list(__calibration_functions.keys())

def get_function(output):
    function, arguments = __calibration_functions[output]
    return function

def get_arguments(output):
    function, arguments = __calibration_functions[output]
    return arguments
