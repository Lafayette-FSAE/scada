import sqlite3

from itertools import zip_longest

conn = sqlite3.connect('example.db')
cursor = conn.cursor()


def log_pdo(node, pdo_data):

	global session

	conn = sqlite3.connect('example.db')
	cursor = conn.cursor()

	pdo_data = list(pdo_data)

	while len(pdo_data) < 8:
		pdo_data.append(None)

	try:
		cursor.execute('''
			INSERT INTO node_{nodename}
			(Session, Byte1, Byte2, Byte3, Byte4, Byte5, Byte6, Byte7, Byte8)
			VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
		'''.format(nodename = node), [session] + pdo_data)

		conn.commit()
		conn.close()
	except:
		pass
		# print('Error: table node_{nodename} does not exist'.format(nodename = node))

# def fetch_process_data(keys, session):

# 	conn = sqlite3.connect('example.db')
# 	cursor = conn.cursor()

# 	for node, key in keys:

# 		conn.execute(''' 
# 			SELECT Byte1, Byte2, Byte3, Byte4, Byte5, Byte6, Byte7, Byte8
# 			FROM node_{nodename} 
# 			WHERE Session = {session}
# 		'''.format(nodename = node,))

def add_node(node, pdo_map):
	global session

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

	)'''.format(nodename=node))

	conn.commit()

	result = pdo_map_changed(node, pdo_map)

	if not result:
		return

	while len(pdo_map) < 8:
		pdo_map.append(None)

	cursor.execute('''INSERT INTO data_map 
		(Node, Session, Byte1, Byte2, Byte3, Byte4, Byte5, Byte6, Byte7, Byte8)
		VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
	''', [node, session] + pdo_map)

	conn.commit()

def pdo_map_changed(node, current_map):
	cursor.execute(''' 
		SELECT Byte1, Byte2, Byte3, Byte4, Byte5, Byte6, Byte7, Byte8
		FROM data_map 
		WHERE Node = ?
		ORDER BY id DESC
		LIMIT 1

	''', [node])

	result = cursor.fetchall()

	if len(result) == 0:
		return True
	else:
		result = result[0]

		for last, current in zip_longest(result, current_map):
			if last != current:
				return True

		return False

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


cursor.execute(''' SELECT Session from events WHERE EventType = 'NEW SESSION' ORDER BY Session DESC LIMIT 1 ''')
session_list = cursor.fetchall()

if len(session_list) == 0:
	session = 1
else:
	# print(session_list[0])
	session, *rest = session_list[0]
	session = session + 1

cursor.execute(''' INSERT INTO events 
	(Session, EventType, EventMsg)
	VALUES (?, 'NEW SESSION', ?)
''', [session, session])


def close():
	conn.close()

# conn.close()