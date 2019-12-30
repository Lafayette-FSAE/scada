import sys
import can
import can_utils
import config
import logging
import scada_logger



bus = can_utils.bus(config.get('bus_info'))
notifier = can.Notifier(bus, [])

if(config.get('emulate_nodes')):

	# append emulators directory to include path
	sys.path.append('emulators')

	# check which emulators are enabled
	if(config.get('emulate_tsi')):
		import tsi_emulator

		tsi = tsi_emulator.Listener(node_id=3)
		notifier.add_listener(tsi)


	if(config.get('emulate_packs')):
		import ams_emulator

		pack1 = ams_emulator.Listener(node_id=1)
		notifier.add_listener(pack1)

		pack2 = ams_emulator.Listener(node_id=2)
		notifier.add_listener(pack2)

	if(config.get('emulate_cockpit')):
		pass

	if(config.get('emulate_motorcontroller')):
		pass


# modules
sys.path.append('modules')
sys.path.append('calibration')

import data_processor
processor = data_processor.Listener(node_id=4)

notifier.add_listener(processor)

sync = can.Message(arbitration_id=0x80, data=0x00)
sync.is_extended_id = False

read = can_utils.messages.sdo_read(node_id=2, index=[0x30, 0x01], subindex=0x02)

master_bus = can_utils.bus(config.get('bus_info'))
master_bus.send_periodic(sync, .1)


# \/				   \/
# \/  GUI Integration  \/
# \/				   \/

from scada_gui import SCADA_GUI
from time import strftime

app = SCADA_GUI()
scada_logger.set_text_window(app.scadaLogScrolledText)

app.set_value('GLV', 'Voltage', '24 V') # Test changing a value

def update_sensors():

	for sensor_group_key in config.get('GUI').get('Sensors'):
		sensor_group = config.get('GUI').get('Sensors').get(sensor_group_key)

		for sensor in sensor_group:
			
			if isinstance(sensor, list):
				
				label, data_key, unit = sensor

				data = can_utils.data_cache.get(data_key)
				
				app.set_value(sensor_group_key, label, '{} {}'.format(data, unit))

	# app.set_value('TSI', 'TS Voltage', '{} V'.format(can_utils.data_cache.get('TSI', 'TS_VOLTAGE')))
	# app.set_value('TSI', 'TS Current', '{} A'.format(can_utils.data_cache.get('TSI', 'TS_CURRENT')))
	# app.set_value('TSI', 'TS Power', '{} kW'.format(can_utils.data_cache.get('SCADA', 'TS_POWER')))
	# app.set_value('Pack 1', 'Voltage', '{} V'.format(can_utils.data_cache.get('PACK1', 'VOLTAGE')))
	# app.set_value('Pack 2', 'Voltage', '{} V'.format(can_utils.data_cache.get('PACK2', 'VOLTAGE')))
	# app.set_value('Pack 1', 'Ambient Temp', '{} C'.format(can_utils.data_cache.get('PACK1', 'AMBIENT_TEMP')))
	# app.set_value('Pack 2', 'Ambient Temp', '{} C'.format(can_utils.data_cache.get('PACK2', 'AMBIENT_TEMP')))
	# app.set_value('Pack 1', 'SOC', '{}%'.format(can_utils.data_cache.get('PACK1', 'SOC_1')))
	# app.set_value('Pack 2', 'SOC', '{}%'.format(can_utils.data_cache.get('PACK2', 'SOC_2')))

class GUIListener(can.Listener):
	def __init__(self, node_id):
		self.node_id = node_id

	def on_message_received(self, msg):
		global needSensorUpdate

		function, node_id = can_utils.messages.get_info(msg)
		
		if function == 'SYNC':
			needSensorUpdate = True

guiListener = GUIListener(node_id=6)
notifier.add_listener(guiListener)

needSensorUpdate = False;
while app.running:
	if needSensorUpdate:
		update_sensors()
		needSensorUpdate = False;
	app.timeValue.set(strftime('%D  %I:%M:%S %p'))
	app.update_idletasks()
	app.update()

app.destroy()
