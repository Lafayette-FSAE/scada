from calibration_utils import cal_function


@cal_function(target='THROTTLE', requires=[
	'MOTOR-3: THROTTLE-byte0',
	'MOTOR-3: THROTTLE-byte1'
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


@cal_function(target='MC_VOLTAGE', requires=['TSI: MOTOR_CONTROLLER_VOLTAGE'])
def mc_voltage(args):
	mc_voltage_raw, *other = args

	return (mc_voltage_raw * 3.14) - 176.39


@cal_function(target='TS_VOLTAGE', requires=['TSI: TS_VOLTAGE'])
def mc_voltage(args):
	voltage_raw, *other = args

	return (voltage_raw * 3.14) - 176.39


@cal_function(target='FLOW_RATE', requires=['TSI: FLOW_RATE'])
def flow_rate(args):
	flow_rate, *other = args

	return flow_rate * 757

"""
Converts ambient temp of pack1 to farenheit because it is 
easy and a good test

"""

# @cal_function(target='PackTemp_Farenheit', requires=['PACK1: AMBIENT_TEMP'])
# def packtemp_farenheit(args):
# 	temp, *other = args

# 	temp_faranheit = temp * (9/5) + 32

# 	return temp_faranheit

# # Calculates the current TS power draw in kW
# @cal_function(target='TS_POWER', requires=[('TSI', 'TS_VOLTAGE'), ('TSI', 'TS_CURRENT')])
# def ts_power(args):
# 	voltage, current, *other = args

# 	power = (voltage * current) / 100

# 	return power

# """
# Calculates Total Tractive System Voltage by adding
# the voltage reported by each pack

# """
# @cal_function(target='TS_VOLTAGE', requires=['PACK1: VOLTAGE', 'PACK2: VOLTAGE'])
# def ts_voltage(args):
# 	pack1, pack2, *other = args

# 	return pack1 + pack2