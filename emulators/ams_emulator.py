import can

bus = can.interface.Bus(bustype='socketcan', channel='vcan0', bitrate='125000')

