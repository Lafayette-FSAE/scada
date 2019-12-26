import can_utils

# print(can_utils.messages.separate_cob_id(0x181))

print(can_utils.messages.get_function(0x180))

print(can_utils.messages.get_code('TPDO'))