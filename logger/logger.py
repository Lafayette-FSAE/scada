#!/usr/bin/python3

import sys, os

sys.path.append('/home/connor/scada/config')

import config
import time
import redis
import pyscopg2

data = redis.Redis(host='localhost', port=6379, db=0)

p = data.pubsub()
p.subscribe('bus_data')
p.subscribe('calculated_data')




## ---------
## SQlite util function
#def create_connection(path):
#		conn = None
#
#		try:
#				conn = sqlite3.connect(path)
#		except Error as e:
#				print(e)
#
##------				
#
## define some sql strings that will get used a lot
#create_table = """
#	create table if not exists {} (
#		id integer primary key,
#		session integer,
#		value real,
#		time datetime default current_timestamp
#	);
#"""
#
#insert_data = """
#	insert into {} (session, value) 
#	values(1, 10.4);
#"""
#
#database = 'database.db'
#def log_data(key, value):
#	conn = sqlite3.connect(database)
#	c = conn.cursor()
#
#	#make sure the table we want to log to exists
#	c.execute(create_table.format(key))
#
#	# append the value to the end of the table
#	c.execute(insert_data.format(key))#, (1, value))
#	conn.commit()
#
#def update(message, value):
##	print('new data event!, {}'.format(message))
#
#	# get the most recent value of SCADA: TSI-THROTTLE
#	throttle = data.get('SCADA: TSI-THROTTLE') 
#	log_data('throttle', throttle)
#
#	for key in data.keys('SCADA:*'):
#		print(key)
#
#while True:
#	message = p.get_message()
#	if message:
#		update(message['channel'], message['data'])
#	
#	time.sleep(0.1)
