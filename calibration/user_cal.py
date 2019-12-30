from calibration_utils import cal_function


"""
Converts ambient temp of pack1 to farenheit because it is 
easy and a good test

"""
@cal_function(target='PackTemp_Farenheit', requires=['PACK1: AMBIENT_TEMP'])
def packtemp_farenheit(args):
	temp, *other = args

	temp_faranheit = temp * (9/5) + 32

	return temp_faranheit

# Calculates the current TS power draw in kW
@cal_function(target='TS_POWER', requires=[('TSI', 'TS_VOLTAGE'), ('TSI', 'TS_CURRENT')])
def ts_power(args):
	voltage, current, *other = args

	power = (voltage * current) / 100

	return power

"""
Calculates Total Tractive System Voltage by adding
the voltage reported by each pack

"""
@cal_function(target='TS_VOLTAGE', requires=['PACK1: VOLTAGE', 'PACK2: VOLTAGE'])
def ts_voltage(args):
	pack1, pack2, *other = args

	return pack1 + pack2