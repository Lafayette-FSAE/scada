from utils import calibration
cal_function = calibration.cal_function

@cal_function(output='motor:throttle', arguments=[
    'motor:throttle:byte0',
    'motor:throttle:byte1'
])
def throttle(args):
	lsb, msb, *other = args
	return msb * 256 + lsb

@cal_function(output='tsi:state', arguments=['tsi:state:int'])
def state(args):
	state_number, *other = args

	if state_number == 1:
		return 'GLV-ON'
	elif state_number == 2:
		return 'AIRS-CLOSED'
	elif state_number == 3:
		return 'DRIVE SETUP'
	elif state_number == 4:
		return 'READY TO DRIVE SOUND'
	elif state_number == 5:
		return 'DRIVE'
	else:
		return 'STATE UNDEFINED'

@cal_function(output='tsi:cooling_temp', arguments=['tsi:cooling_temp:raw'])
def temp(args):
	val, *rest = args
	voltage = (val / 255) * 3.3
	return (20.439 * voltage * voltage) - (109.78 * voltage) + 153.61

@cal_function(output='tsi:mc_voltage', arguments=['tsi:mc_voltage:raw'])
def mc_voltage(args):
	mc_voltage_raw, *other = args
	return (((mc_voltage_raw / 255) * 5) - 1.28) * 61

@cal_function(output='tsi:voltage', arguments=['tsi:voltage:raw'])
def ts_voltage(args):
	voltage_raw, *other = args
	return (((voltage_raw / 255) * 5) - 1.28) * 61

@cal_function(output='tsi:throttle', arguments=['tsi:throttle:raw'])
def throttle(args):
	throttle_raw, *other = args
	voltage = (throttle_raw / 255) * 3.3
	return voltage * 33 / 18

@cal_function(output='tsi:flow_rate', arguments=['tsi:flow_rate:raw'])
def flow_rate(args):
	flow_rate, *other = args
	if flow_rate == 0:
		return 0
	else:
		return 0.0535 + 757.5 * (1/flow_rate)

@cal_function(output='pack1:temp:farenheit', arguments=['pack1:temp'])
def packtemp_farenheit(args):
	temp, *other = args
	temp_faranheit = temp * (9/5) + 32
	return temp_faranheit

# Calculates the TS power draw in kW
@cal_function(output='tsi:power', arguments=['tsi:voltage', 'tsi:current'])
def ts_power(args):
	voltage, current, *other = args
	power = (voltage * current) / 100
	return power
