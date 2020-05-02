#!/usr/bin/python3

import sys, os

sys.path.append('/home/connor/scada/config')

import config
import time
import redis
import psycopg2

car_state = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)
database = psycopg2.connect(
	user='fsae',
	password='cables',
	host='localhost',
	port='5432',
	database = 'demo'
)

p = car_state.pubsub()
p.subscribe('bus_data')
p.subscribe('calculated_data')

cursor = database.cursor()

cursor.execute(""" 
	DROP TABLE IF EXISTS sensors;
	DROP TABLE IF EXISTS data;
""")

cursor.execute("""
	CREATE TABLE IF NOT EXISTS data(
		id SERIAL PRIMARY KEY,
		sensor_id VARCHAR(255) NOT NULL,
		value VARCHAR(255),
		timestamp TIMESTAMP DEFAULT NOW()
	);
""")

cursor.execute("""
	CREATE TABLE IF NOT EXISTS sensors(
		id SERIAL PRIMARY KEY,
		redis_key VARCHAR(255) NOT NULL UNIQUE,
		display_name VARCHAR(255),
		datatype VARCHAR(255),
		unit VARCHAR(255)
	);		  
""")

database.commit()

previous_values = {}

def update(message, key):
	if car_state.get(key) == previous_values.get(key, None):
		return

	ignore_keys = []
	for key_string in config.get('dont_log', []):
		ignore_keys = ignore_keys + car_state.keys(key_string)
		
	if not key in ignore_keys:
		cursor.execute("""
			INSERT INTO sensors
			(redis_key)
			VALUES (%s)
			ON CONFLICT (redis_key) DO NOTHING
		""", [key])
		
		cursor.execute("""
			INSERT INTO data (sensor_id, value)
			VALUES (%s, %s)
		""", [key, car_state.get(key)])

		previous_values[key] = car_state.get(key)

while True:
	message = p.get_message()
	if message:
		if message['channel'] in ['bus_data', 'calculated_data']:  
			update(message['channel'], message['data'])
	else:
		database.commit()
		time.sleep(0.1)
