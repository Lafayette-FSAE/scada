import logging
import logging.handlers




# import redis

# database = redis.Redis(host='localhost', port=6379, db=0)


# """
# level should be one of:
# 	debug
# 	info
# 	warning
# 	error
# """
# def syslog(level, message):
# 	timestamp, _ = database.time()
# 	database.set(f'logs:{level}:{timestamp}', message)