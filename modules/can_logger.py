# import can
# import can_messages

import sqlite3
# import config

conn = sqlite3.connect('example.db')
cursor = conn.cursor()

cursor.execute('''CREATE TABLE IF NOT EXISTS example_node(

	id INTEGER PRIMARY KEY,
	Session INTEGER,

	Byte1 INTEGER,
	Byte2 INTEGER,
	Byte3 INTEGER,
	Byte4 INTEGER,
	Byte5 INTEGER,
	Byte6 INTEGER,
	Byte7 INTEGER,
	Byte8 INTEGER,

	Timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
)''')

cursor.execute('''CREATE TABLE IF NOT EXISTS data_map(

	id INTEGER PRIMARY KEY,
	Session INTEGER,
	Node TEXT,

	Byte1 TEXT,
	Byte2 TEXT,
	Byte3 TEXT,
	Byte4 TEXT,
	Byte5 TEXT,
	Byte6 TEXT,
	Byte7 TEXT,
	Byte8 TEXT,

	Timestamp DATETIME DEFAULT CURRENT_TIMESTAMP

)''')

cursor.execute('''CREATE TABLE IF NOT EXISTS events(

	id INTEGER PRIMARY KEY,
	Session INTEGER,
	Node TEXT,

	EventType TEXT,
	EventMsg TEXT,

	Timestamp DATETIME DEFAULT CURRENT_TIMESTAMP

)''')

cursor.execute('''
	INSERT INTO data_map (Session, Node, Byte1, Byte2, Byte3, Byte4, Byte5, Byte6)
	VALUES (1, 'tsi', 'COOLING_TEMP_1', 'COOLING_TEMP_2', 'FLOWRATE', 'STATE', 'TS_CURRENT', 'TS_VOLTAGE')
 ''')

conn.commit()

def add_node(nodename, pdo_map):
	cursor.execute('''CREATE TABLE IF NOT EXISTS node_{nodename}(

		id INTEGER PRIMARY KEY,
		Session INTEGER,

		Byte1 INTEGER,
		Byte2 INTEGER,
		Byte3 INTEGER,
		Byte4 INTEGER,
		Byte5 INTEGER,
		Byte6 INTEGER,
		Byte7 INTEGER,
		Byte8 INTEGER,

		Timestamp DATETIME DEFAULT CURRENT_TIMESTAMP

	)'''.format(nodename=nodename))

	conn.commit()

	# Check to see if the process data map has changed
	cursor.execute(''' 
		SELECT Byte1, Byte2, Byte3, Byte4, Byte5, Byte6, Byte7, Byte8
		FROM data_map 
		WHERE Node = ?
		ORDER BY Session DESC
		LIMIT 1

	''', [nodename])

	rows = cursor.fetchall()

	for row in rows:
		print(rows)


def get_current_session():
	return 1

add_node('tsi', None)

conn.close()

"""
Reads Data from the CAN bus and writes it to a database

"""

# class Listener(can.Listener):
# 	def __init__(self, bus, node_id):
# 		self.bus = bus
# 		self.node_id = node_id

# 	def on_message_received(self, msg):

# 		function, node = can_messages.separate_cob_id(msg.arbitration_id)

# 		# Deal with TPDOs
# 		if function == 0x180:
# 			pass