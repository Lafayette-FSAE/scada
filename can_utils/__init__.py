import can_utils.messages
import can_utils.object_dictionary

ObjectDictionary = object_dictionary.ObjectDictionary


import can

def bus(bus_info):

	try:
		bustype = bus_info['bustype']
	except:
		return


	if bustype == 'virtual':
		return can.interface.Bus('main', bustype=bustype)

	elif bustype == 'socketcan':
		return can.interface.Bus(bustype='socketcan', channel=bus_info['channel'], bitrate=bus_info['bitrate'])

	# if bustype == 'virtual':
	# 	return can.interface.Bus('main', bustype='virtual')

	# elif bustype == 'vcan':
	# 	return can.interface.Bus(bustype='socketcan', channel='vcan0', bitrate=125000)

	# elif bustype == 'can':
	# 	return can.interface.Bus(bustype='socketcan', channel='can0', bitrate=125000)

	# else:
	# 	print("bustype must be either 'virtual', 'vcan', or 'can'")
	# 	pass