# SCADA
Project Kalman part 2, Supervisory Control And Data Acquisition written in python for the Lafayette FSAE Car

## Configuration
---

Config settings can be changed by editing config.yaml in the root directory

### Bus Setup

If you are running SCADA on a system without a CAN interface, set bustype to virtual.

Virtual CAN networking can also be acheived by using the vcan0 channel of socketcan.

As it is currently configured, the raspberry pi in the Dyno room talks to the rest of
the network on the can0 channel of socketcan with a bitrate of 125000

If bustype is set to virtual, channel and bitrate fields can be omitted

```yaml
bus_info:
  bustype: socketcan | virtual
  channel: can0 | vcan0 | (or any other socketcan channel)
  bitrate: 125000
```

### Emulation

SCADA offers the ability to emulate other nodes on the CAN network in order to simplify testing.
While the current behavior is crude, there is a lot of potential for improvement.

Turn this behavior on or off with the emulate_nodes field, or selectively enable or disable
each node with the node specific fields

It is not recommended to emulate nodes that are currently running on the bus

```yaml
emulate_nodes: yes

emulate_tsi: yes
emulate_packs: yes
emulate_cockpit: no
emulate_motorcontroller: no
```

### Data

Most data is sent over the bus in 8 byte CAN packets called Process Data Objects, or PDOs,
with each byte representing a different piece of from that node.

The process_data fields tells SCADA where to expect each piece of data in each packet

If the node listed is either SCADA itself, of one of the emulated nodes, this field will be used
to define the behavior of its PDO when it is generated.

```yaml
process_data:
  TSI:    [ COOLING_TEMP_1, COOLING_TEMP_2, FLOWRATE, STATE, TS_CURRENT, TS_VOLTAGE ]
  PACK1:  [ VOLTAGE, CURRENT, SOC_1, SOC_2, AMBIENT_TEMP, 'MIN_CELL_TEMP', AVG_CELL_TEMP, MAX_CELL_TEMP ]
  PACK2:  [ VOLTAGE, CURRENT, SOC_1, SOC_2, AMBIENT_TEMP, MIN_CELL_TEMP, AVG_CELL_TEMP, MAX_CELL_TEMP ]
  SCADA:  [ TS_POWER ]
```

TODO: it should be possible to define pieces of data that are more than 1 byte long

TODO: need a good way to describe nodes with more than one PDO


Because not all data needs to be read at a high frequency, the CANopen standard defines a way to
read and write data at arbitrary times, called the Service Data Object.

Each piece of data has a unique two byte index and a one byte subindex, and can be read with a special CAN packet

The service_data field defines a list of data that needs be be manually polled in this way. Each piece of data needs
to have a node_id, index, subindex, and poll_rate

```yaml
service_data:

  Cell1Temp:
    node_id: 2
    index: 2011
    poll_rate: 10

  MotorTemp:
    node_id: 1
    index: 2010
    subindex: 0
    poll_rate: 0.5
```

NOTE: it is important to remember that not all nodes on the bus will support this,
but the Motor Controller definitely will.

A complete description of all data that can be accessed from the motor controller can be found
[here](https://docplayer.net/48431275-Emdrive-firmware-specifications.html)

Further reading on Service Data and Process Data can be found
[here](http://www.byteme.org.uk/canopenparent/canopen/sdo-service-data-objects-canopen/)
and
[here](http://www.byteme.org.uk/canopenparent/canopen/pdo-process-data-objects-canopen/)

