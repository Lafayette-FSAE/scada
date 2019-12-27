import can_utils

from can_utils import object_dictionary as OD

od = OD.ObjectDictionary()

od.add_key('TEMP')
od.add_key('VOLTAGE')
od.add_key('STATE_OF_CHARGE')
od.add_key('CURRENT')

od.set_pdo_map(['CURRENT', 'STATE_OF_CHARGE', 'TEMP', 'VOLTAGE'])



# print(od)

pdo = od.get_pdo_data()
# print(od.get_value('TPDO1_LENGTH'))

# print(od)

print(pdo)

# print(can_utils.messages.get_function(0x180))
# print(can_utils.messages.get_code('TPDO'))