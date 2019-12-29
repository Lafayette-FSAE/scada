import can
import can_utils

import config

# bus = can.interface.Bus(bustype='socketcan', channel='vcan0', bitrate='125000')
# bus = can.interface.Bus('main', bustype='virtual')

bus = can_utils.bus(config.get('bus_info'))

od = can_utils.ObjectDictionary()

od.add_key('AMBIENT_TEMP')
od.add_key('VOLTAGE')
od.add_key('TS_CURRENT')
od.add_key('CHARGING_CURRENT')

od.add_key('SEGMENT_01_TEMPS', index=0x3001)
od.add_key('CELL_01_TEMP', index=0x3001, subindex=0x00)
od.add_key('CELL_02_TEMP', index=0x3001, subindex=0x01)
od.add_key('CELL_03_TEMP', index=0x3001, subindex=0x02, value=25)
od.add_key('CELL_04_TEMP', index=0x3001, subindex=0x03)
od.add_key('CELL_05_TEMP', index=0x3001, subindex=0x04)
od.add_key('CELL_06_TEMP', index=0x3001, subindex=0x05)
od.add_key('CELL_07_TEMP', index=0x3001, subindex=0x06)
od.add_key('CELL_08_TEMP', index=0x3001, subindex=0x07)

od.add_key('SEGMENT_02_TEMPS', index=0x3002)
od.add_key('CELL_09_TEMP', index=0x3002, subindex=0x00)
od.add_key('CELL_10_TEMP', index=0x3002, subindex=0x01, value=8)
od.add_key('CELL_11_TEMP', index=0x3002, subindex=0x02, value=25)
od.add_key('CELL_12_TEMP', index=0x3002, subindex=0x03)
od.add_key('CELL_13_TEMP', index=0x3002, subindex=0x04)
od.add_key('CELL_14_TEMP', index=0x3002, subindex=0x05)
od.add_key('CELL_15_TEMP', index=0x3002, subindex=0x06)
od.add_key('CELL_16_TEMP', index=0x3002, subindex=0x07)

od.add_key('SEGMENT_01_VOLTAGES', index=0x3003)
od.add_key('CELL_01_VOLTAGE', index=0x3003, subindex=0x00)
od.add_key('CELL_02_VOLTAGE', index=0x3003, subindex=0x01)
od.add_key('CELL_03_VOLTAGE', index=0x3003, subindex=0x02)
od.add_key('CELL_04_VOLTAGE', index=0x3003, subindex=0x03)
od.add_key('CELL_05_VOLTAGE', index=0x3003, subindex=0x04)
od.add_key('CELL_06_VOLTAGE', index=0x3003, subindex=0x05)
od.add_key('CELL_07_VOLTAGE', index=0x3003, subindex=0x06)
od.add_key('CELL_08_VOLTAGE', index=0x3003, subindex=0x07)

od.add_key('SEGMENT_02_VOLTAGES', index=0x3004)
od.add_key('CELL_09_VOLTAGE', index=0x3004, subindex=0x00)
od.add_key('CELL_10_VOLTAGE', index=0x3004, subindex=0x01)
od.add_key('CELL_11_VOLTAGE', index=0x3004, subindex=0x02)
od.add_key('CELL_12_VOLTAGE', index=0x3004, subindex=0x03)
od.add_key('CELL_13_VOLTAGE', index=0x3004, subindex=0x04)
od.add_key('CELL_14_VOLTAGE', index=0x3004, subindex=0x05)
od.add_key('CELL_15_VOLTAGE', index=0x3004, subindex=0x06)
od.add_key('CELL_16_VOLTAGE', index=0x3004, subindex=0x07)

od.set_pdo_map(['AMBIENT_TEMP', 'VOLTAGE', 'TS_CURRENT'])

def update():
	pass

class Listener(can.Listener):
	def __init__(self, node_id):
		self.node_id = node_id

	def on_message_received(self, msg):

		print('msg received')

		function, node = can_utils.messages.get_info(msg)

		# sync
		if function == 'SYNC':
			print('test')
			update()			

		# sdo read
		if function == 'SDO-READ' and node == self.node_id:

			command = msg.data[0]
			index = int.from_bytes(msg.data[1:3], byteorder='big')
			subindex = msg.data[3]

			value = od.get_value('', index=(index, subindex))

			new_index = [msg.data[1], msg.data[2]]
			response = can_utils.messages.sdo_response(self.node_id, new_index, subindex, value)
			bus.send(response)

			
