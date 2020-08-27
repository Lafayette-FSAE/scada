#!/usr/bin/python3

# TODO: calls updates of emulators manually

import sys, os
import time

sys.path.append('/home/fsae/scada')
sys.path.append('/home/fsae/scada/emulator')

sys.path.append('/usr/etc/scada')
sys.path.append('/usr/etc/scada/config')

import can
import utils

from utils import object_dictionary
from utils import messages

import config

bus = utils.bus(config.get('bus_info'))
notifier = can.Notifier(bus, [])

import redis
data = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)	
p = data.pubsub()
p.subscribe('restart-emulators')

import tsi_emulator
#import ams_emulator

# Add emulators to the bus
#notifier.add_listener(tsi_emulator.Listener(node_id = 3))
#notifier.add_listener(ams_emulator.Listener(node_id = 4))

#notifier.add_listener(ams_emulator.Listener(node_id = 5))
# TODO: separate emulators of the same type should not 
#       share a state, second pack should remain commented
#       out until this gets fixed


# Make this the bus's sync producer
sync = can.Message(arbitration_id=0x80, data=0x00)
sync.is_extended_id = False
bus.send_periodic(sync, 0.1)

# Main update loop, just tell the emulators to update their states
# and wait for a short amount of time
while True:
    # on reset signal
    if p.get_message():
        data.set('emulator:simulation_time', 0)
        data.publish('new-session', 0)

    #ams_emulator.update()
    tsi_emulator.update()
    tsi_emulator.send_pdo()
    time.sleep(0.5)
