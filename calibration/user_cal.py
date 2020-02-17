from calibration_utils import cal_function


@cal_function(target='THROTTLE', requires=[
	'MOTOR: THROTTLE-byte0',
	'MOTOR: THROTTLE-byte1'
])
def throttle(args):
	lsb, msb, *other = args

	return msb * 256 + lsb

"""
Converts TSI state integer to human readable string

"""

@cal_function(target='STATE', requires=['TSI: STATE'])
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


@cal_function(target='COOLING_TEMP', requires=['TSI: COOLING_TEMP_1'])
def temp(args):
	val, *rest = args

	voltage = (val / 255) * 3.3
	return (20.439 * voltage * voltage) - (109.78 * voltage) + 153.61

@cal_function(target='MC_VOLTAGE', requires=['TSI: MC_VOLTAGE'])
def mc_voltage(args):
	mc_voltage_raw, *other = args
	return (((mc_voltage_raw / 255) * 5) - 1.28) * 61


@cal_function(target='TS_VOLTAGE', requires=['TSI: TS_VOLTAGE'])
def ts_voltage(args):
	voltage_raw, *other = args

	return (((voltage_raw / 255) * 5) - 1.28) * 61


@cal_function(target='THROTTLE-TSI', requires=['TSI: THROTTLE'])
def throttle(args):
	throttle_raw, *other = args
	
	voltage = (throttle_raw / 255) * 3.3
	return voltage * 33 / 18

@cal_function(target='FLOW_RATE', requires=['TSI: FLOW_RATE'])
def flow_rate(args):
	flow_rate, *other = args

	if flow_rate == 0:
		return 0
	else:
		return 0.0535 + 757.5 * (1/flow_rate)

"""
Converts ambient temp of pack1 to farenheit because it is 
easy and a good test

"""

# @cal_function(target='PackTemp_Farenheit', requires=['PACK1: AMBIENT_TEMP'])
# def packtemp_farenheit(args):
# 	temp, *other = args

# 	temp_faranheit = temp * (9/5) + 32

# 	return temp_faranheit

# Calculates the current TS power draw in kW
@cal_function(target='TS_POWER', requires=[('TSI', 'TS_VOLTAGE'), ('TSI', 'TS_CURRENT')])
def ts_power(args):
	voltage, current, *other = args

	power = (voltage * current) / 100

	return power
