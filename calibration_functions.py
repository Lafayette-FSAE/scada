
@cal_function(target='PackTemp_Farenheit', requires=['PackTemp'])
def packtemp_farenheit(args):
	temp, *other = args

	return temp * (9/5) + 32

@cal_function(target='Net_State_Of_Charge', requires=['Pack1-SOC', 'Pack2-SOC'])
def net_soc(args):
	pack1, pack2, *other = args

	return pack1 + pack2