from calibration_utils import cal_function


"""
Converts ambient temp of pack1 to farenheit because it is 
easy and a good test

"""
@cal_function(target='PackTemp_Farenheit', requires=['pack1 - ambient_temp'])
def packtemp_farenheit(args):
	temp, *other = args

	temp_faranheit = temp * (9/5) + 32

	return temp_faranheit


@cal_function(target='TS_POWER', requires=['tsi - TS_VOLTAGE', 'tsi - TS_CURRENT'])
def ts_power(args):
	voltage, current, *other = args

	power = (voltage * current) / 100

	return power

"""
Calculates Total Tractive System Voltage by adding
the voltage reported by each pack

"""
@cal_function(target='TSVoltage', requires=['pack1 - voltage', 'pack2 - voltage'])
def ts_voltage(args):
	pack1, pack2, *other = args

	return pack1 + pack2