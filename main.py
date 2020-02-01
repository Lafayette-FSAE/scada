import sys
import can
import can_utils
import config
import logging
import scada_logger

from can_utils import data_cache

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
sys.path.append('interfaces')

import data_processor
processor = data_processor.Listener(node_id=4)

notifier.add_listener(processor)

sync = can.Message(arbitration_id=0x80, data=0x00)
sync.is_extended_id = False

read = can_utils.messages.sdo_read(node_id=2, index=[0x30, 0x01], subindex=0x02)

master_bus = can_utils.bus(config.get('bus_info'))
master_bus.send_periodic(sync, .1)

# for message in bus:
# 	pass

import tui

term = tui.term



with term.fullscreen():
	for message in bus:

		tui.data = [
			('State', 				data_cache.get('SCADA: STATE')),
			('MC Voltage', 			data_cache.get('SCADA: MC_VOLTAGE')),
			('TS Voltage', 			data_cache.get('SCADA: TS_VOLTAGE')),
			('Cooling Temp 1', 		data_cache.get('TSI: COOLING_TEMP_1')),
			('Cooling Temp 2', 		data_cache.get('TSI: COOLING_TEMP_1')),
			('Flow Rate', 			data_cache.get('SCADA: FLOW_RATE')),
			('Throttle', 			data_cache.get('MOTOR3: THROTTLE')),	
		]
		

		tui.print_column(tui.data, label="TSI")

# \/				   \/
# \/  GUI Integration  \/
# \/				   \/

# from scada_gui import SCADA_GUI

# app = SCADA_GUI()
# scada_logger.set_text_window(app.scadaLogScrolledText)

# def update_sensors():
# 	for sensor_group_key in config.get('GUI').get('Sensors'):
# 		sensor_group = config.get('GUI').get('Sensors').get(sensor_group_key)
# 		for sensor in sensor_group:
# 			data_key = sensor_group.get(sensor).get('data_target')
# 			if data_key:
# 				data = can_utils.data_cache.get(data_key)
# 				unit = sensor_group.get(sensor).get('unit')
# 				oprange = sensor_group.get(sensor).get('oprange')
# 				app.update_value(sensor_group_key, sensor, data, unit, oprange)


# class GUIListener(can.Listener):
# 	def __init__(self, node_id):
# 		self.node_id = node_id

# 	def on_message_received(self, msg):
# 		global needSensorUpdate

# 		function, node_id = can_utils.messages.get_info(msg)
		
# 		if function == 'SYNC':
# 			needSensorUpdate = True

# guiListener = GUIListener(node_id=6)
# notifier.add_listener(guiListener)

# needSensorUpdate = False;
# while app.running:
# 	if needSensorUpdate:
# 		update_sensors()
# 		app.update_plot()
# 		needSensorUpdate = False;
# 	# app.timeValue.set(strftime('%D  %I:%M:%S %p'))
# 	app.update_idletasks()
# 	app.update()

# app.destroy()
