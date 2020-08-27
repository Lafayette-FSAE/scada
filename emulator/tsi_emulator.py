#!/usr/bin/python3

import sys, os
import can
import math

import redis
data = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)	

import utils
from utils import object_dictionary
from utils import messages

import config

bus = utils.bus(config.get('bus_info'))
notifier = can.Notifier(bus, [])

# Create Object Dictionary
pdo_structure = config.get('process_data')['TSI']

od = object_dictionary.ObjectDictionary()
od.add_keys(pdo_structure)
od.set_pdo_map(pdo_structure)

od.set('state:int', 1)
data.set('emulator:simulation_time', 0)
data.publish('new-session', 0)

state_transitions = [5, 10, 30, 35, 40]
def get_state(time):
	global state_transitions
	temp = state_transitions.copy()
	temp.append(time)
	temp.sort()
	
	return temp.index(time)
	
# Calculate the value of the precharge
# curve at a given point in time
def precharge_curve(time):
	return 100 * (1 - math.exp(-1 * 0.25 * time))

def fix_voltage(v):
	return int((((v / 61) + 1.28) / 5) * 255)

def update():
	time = data.incr('emulator:simulation_time')
	state = get_state(time)
	od.set('state:int', state)

	# GLV-OFF
	if state == 0:
		od.set('voltage:raw', fix_voltage(0))
		od.set('mc_voltage:raw', fix_voltage(0))
		od.set('throttle:raw', 0)

	# GLV-ON
	if state == 1:
		od.set('voltage:raw', fix_voltage(0))
		od.set('mc_voltage:raw', 0)
		od.set('throttle:raw', 0)

	# PRECHARGE
	if state == 2:
		elapsed_time = time - state_transitions[1]
		mc_voltage = precharge_curve(elapsed_time)

		od.set('voltage:raw', fix_voltage(100))
		od.set('mc_voltage:raw', fix_voltage(mc_voltage))
		od.set('throttle:raw', 0)

	# DRIVE SETUP
	if state == 3:
		od.set('voltage:raw', fix_voltage(100))
		od.set('mc_voltage:raw', fix_voltage(100))
		od.set('throttle:raw', 0)

	# READY TO DRIVE SOUND
	if state == 4:
		od.set('voltage:raw', fix_voltage(100))
		od.set('mc_voltage:raw', fix_voltage(100))
		od.set('throttle:raw', 0)
		
	# DRIVE
	if state == 5:
		od.set('voltage:raw', fix_voltage(100))
		od.set('mc_voltage:raw', fix_voltage(100))
		od.set('throttle:raw', int(127 * (1 + math.sin(time / 180))))

node_id = 3
def send_pdo():
	data = od.get_pdo_data()
	message = messages.pdo(node_id, data)
	bus.send(message)
