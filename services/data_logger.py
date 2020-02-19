import sys, os

scada_path = os.environ['SCADA_PATH']
sys.path.append(scada_path)
# sys.path.append(f'{scada_path}/calibration')

import config
import redis
import time

client = redis.Redis(host='localhost', port=6379, db=0)

subsciber = client.pubsub()
subsciber.subscribe('new_data')

def update():
	throttle = client.get('TSI: THROTTLE')
	client.lpush('lists:throttle', f'{time.time()}:{throttle}')

while True:
	if subsciber.get_message():
		update()

	time.sleep(0.1)