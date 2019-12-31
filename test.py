# import can_utils

# from can_utils import object_dictionary as OD

# od = OD.ObjectDictionary()

# od.add_key('TEMP')
# od.add_key('VOLTAGE')
# od.add_key('STATE_OF_CHARGE')
# od.add_key('CURRENT')

# od.set_pdo_map(['CURRENT', 'STATE_OF_CHARGE', 'TEMP', 'VOLTAGE'])



# # print(od)

# pdo = od.get_pdo_data()
# # print(od.get_value('TPDO1_LENGTH'))

# # print(od)

# print(pdo)

# # print(can_utils.messages.get_function(0x180))
# # print(can_utils.messages.get_code('TPDO'))

import yaml

config = {}

with open('test_config.yaml', 'r') as stream:
		try:
			config = yaml.safe_load(stream)
		except yaml.YAMLError as exc:
			print(exc)

# print(config)
sensors = config.get('GUI').get('Sensors')
# print(sensors)
l = list(sensors)
print(l)
glv = sensors.get('GLV')
print(glv)
l2 = list(glv)
print(l2)
print(sensors.get('GLV').get('Voltage').get('data_target'))