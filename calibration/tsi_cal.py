from calibration_utils import cal_function

"""
Calibrates flowrate from raw value reported by tsi
into Liters per minute

"""
# @cal_function(target='FLOWRATE', requires=['TSI: FLOWRATE_RAW'])
def packtemp_farenheit(args):
	flowrate_raw, *other = args

	return flowrate_raw * 0.0535 + 0.1212