from calibration_utils import cal_function


@cal_function(target='PackTemp_Farenheit', requires=['pack1 - ambient_temp'])
def packtemp_farenheit(args):
	temp, *other = args

	temp_faranheit = temp * (9/5) + 32

	return temp_faranheit

@cal_function(target='TSVoltage', requires=['pack1 - voltage', 'pack2 - voltage'])
def ts_voltage(args):
	pack1, pack2, *other = args

	return pack1 + pack2