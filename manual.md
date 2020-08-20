# SCADA

## User Manual
---

# Introduction and Purpose

SCADA is an acronym for Supervisory Control And Data Aquisition. It is a term borrowed from industrial control applications, where a single server is often used to oversee large industrial plants such as oil refineries and assembly lines. In general, SCADA systems have three functions, they aquire data from the network of sensors connected to the plant, send control signals to the plant's other subsystems, and provide an interface for humans to interact with the plant by viewing aggregated data and issueing commands.

The Lafayette FSAE team has been working to develop a SCADA system that can be fully integrated into its electric vehichle, with the goal of performing all of the above three functions both during normal operation and throughout the various testing and maintenacne procedures that it will undergo. At times in the past, this system has been referred to as VSCADA, short for Vehichle SCADA, to distinguish it from the industrial systems described above, but for brevity this document will refer to it simply as SCADA.

# Design Overview

## CAN Network

The existence of a SCADA system implies a network. There must be communication taking place between SCADA and the other subsystems for it to succesfully perform any of its responsibilities. There are a number of network protocols to choose from, but the defacto standard for automotive use is CAN (Controller Area Network) and so that is what is used in the Lafayette FSAE Car.

A good explanation of CAN can be found here:

[https://www.csselectronics.com/screen/page/simple-intro-to-can-bus/language/en](https://www.csselectronics.com/screen/page/simple-intro-to-can-bus/language/en)

At the time of writing, the CAN Network contains between 6 and 7 nodes, depending whether an external pc is needed to configure and operate the motor controller. They are:

- Motor Controller
- SCADA
- Battery Packs (1 and 2)
- TSI
- DashMan
- External Configuration PC

### CANOpen

CAN is a very low level protocol. It defines a way for a node to broadcast up to 8 bytes of data and an ID, but very few of the other things needed to perform sophisticated network operations. For this, a higher level protocol needs to be defined on top of CAN, and currently there are several competing standards. These have been described as the equivilant of something like http to the tcp/ip stack, adding an additional layer of abstraction for easier use.

While it is not the most popular, the Lafayette FSAE team has chosen the CANOpen Standard for its vehichle in order to match that of the already purchased Motor Controller, which includes a rich set of CANOpen based tools.

CANOpen can also be thought of as a subset of CAN, meaning if a node is added to the network that does not comply with the CANOpen standard, the behavior of the other nodes is undefined. For this reason, it is very important that every node added to the network, even if it does not intend to make use of the full set of CANOpen features, at least comply with a subset of the protocol.

Here are some good resources for learning more about the protocol:

[https://www.can-cia.org/canopen/](https://www.can-cia.org/canopen/)

[https://www.youtube.com/watch?v=DlbkWryzJqg](https://www.youtube.com/watch?v=DlbkWryzJqg)

As a supplement to these resources, a brief description of CANOpen is also provided here:

CANOpen can best be thought of as the sum of several communication protocols, coupled with some defined behavior for each node.

## Hardware

SCADA runs on a Raspberry Pi that is mounted inside of the CarMan enclosure. Attached to it is a "hat" that enables CAN communication and provides a pass through for the Pi's GPIO pins. Together, these are connected to the GLV board via a set of 3 cables: A micro USB cable for power, DB9 serial cable for CAN high and low signals, and a homemade ribbon cable for certain GPIO pins. Additional cables can be run to connect the Pi to other parts of the car and/or Dyno Room. These include:

- Ribbon Cable to the CarMan Display
- HDMI to to the Dyno Room Monitor
- USB to external keyboard and mouse
- USB to the dynamometer

***author's note***

The three cables connecting the SCADA Pi to the GLV board are a bad design decision and should be removed at the next possible opportunity. With the exception of the DB9, these cables and their connectors are not rated for automotive use, and could easily become disconnected during heavy vibrations and render SCADA inoperable. In addition, the adjacency of the SCADA Pi and the GLV Board within the CarMan enclosure make these cables appear comically large, forcing space to be used for cable routing that could otherwise be taken up by something more useful. It would be a far better solution to integrate the SCADA Pi and the CAN hat into the GLV board.

### Alternative Hardware

## Software

The most important thing to understand about the design of SCADA in its current form is that it is not a single program, but rather a system of programs which are made to run concurrently and interface with eachother. These programs try as much as possible to abide by the unix philosophy of software development, which is in essence, to write programs that are extremely limited in scope, and that interact well with each other, through standard, well defined interfaces. This is opposed to the way that SCADA has been written in the past, where a single large, integrated program is made to implement all the features required by the system. There are some drawbacks to the small and modular approach, which will be addressed later, but also a lot of advantages. They include the following:

- Features can usually be added without having to modify existing code, this can help to mitigate the square law of adding features to things.

- SCADA can be written in multiple different languages, so the best language can always be chosen for a given purpose, without having to make compromises.

- When the purpose of a program is general enough, existing open source software can be used instead of writing an in house solution.

- The individual components of the system are easy to understand and reason about.

- When problems arise, they are easy to isolate and diagnose. 

The programs making up SCADA and their structure are described in the following diagram. They are organized into a pipeline, with data flowing from one service to the next in a well defined way. Each service has a specific roll in either organizing or transforming the data so that it can be made sense of by the user.

![](https://raw.githubusercontent.com/Lafayette-FSAE/scada/master/diagrams/data-aquisition.svg)

What follows is a short description of each service and its function.

### Sorter

The sorter listens to the CAN bus for incoming messages, upon receiving a message, it checks its ID and Structure against a config file to generate an associated set of key value pairs. It then writes these key value pairs into the Redis cache and sends a message to the calibrator that new data has been received. The sorter is the only service that is aware of CAN or CANOpen, meaning SCADA can be made to work with a different networking protocol, or more than one, simply by switching out the sorter service or adding an additional one, without affecting any services downstream.

### Calibrator

The calibrator is responsible for translating the raw data read by the sorter from the CAN bus into a more human readable form. This is usually a case of linear calibration of raw sensor data, such as with the TSI node, or the recombining of data that was transmitted as multiple bytes, like with the Throttle value reported by Motor Controller. However, it can be made to support calculations of arbitrary complexity, such as for example, the calculation of power from a given voltage and current, the averaging of multiple sensors, filtering, differentiation, and so on. All calibrator operations are defined by the user as functions in the user_cal.py file. Once data is calculated, it is written back into the Redis server as a different key.

### Logger

The logger takes the data gathered by the sorter and calculated by the calibrator and logs a subset of it into the Postgresql database at regular intervals. The subset of data to be logged is defined in config.yaml file.

It samples the data at regular intervals, and performs some basic logic to limit the database to only storing useful data. In general, it it tries to only log data that is changing, so as not to flood the database with constant values. The logger writes all logged data to a single sql table, called `data`, with the following columns:

- id
- sensor_id
- value
- timestamp

In keeping with the unix tradition, all data is stored in the same way as text. Programs reading from the database are responsible for translating the data into its expected type. A companion table, called `sensors` is included in the database to store metadata about each sensor. It has columns:

- id
- redis_key (equivilant to sensor_id, one of these should probably be renamed)
- display_name
- datatype
- unit

### Redis

For the most part, programs communicate with eachother via Redis. Redis is an open source, in memory database that stores data as key value pairs, it also functions as a basic communications bus for sending simple inter-service messages.

[https://redis.io/](https://redis.io/)

### Postgres

If a program needs to write non-volitile data, it does so using an SQL database via a Postgres server. 

[https://www.postgresql.org/](https://www.postgresql.org/)

### Concurrency

Concurrency is handled by the operating system via systemd. All programs which are meant to be run as a service have an associated .service file, and can be managed with the systemctl interface.

All services are single threaded and should consist of only one update loop, delay statements are inserted into the loop in order to release the cpu for use by other services.

[https://www.digitalocean.com/community/tutorials/how-to-use-systemctl-to-manage-systemd-services-and-units](https://www.digitalocean.com/community/tutorials/how-to-use-systemctl-to-manage-systemd-services-and-units)


### Clients

Both the Redis and Postgres servers expose TCP ports, and any software capable of interacting with these TCP ports can be considered a SCADA client. These clients can be run either locally on the SCADA Pi or remotely over a network. There are already a number of SCADA clients to choose from, and the best one for any given application will depend largely on circumstance and preference.

One potential 3rd party client that comes very highly recommended is Grafana. Grafana is an open source data viewing and monitoring tool that specializes in the construction of a wide range of data visualizations such as graphs, gauges, statistics, and logs based on a number of potential data sources. It supports Postgresql out of the box and is extremely easy to set up. It also has a rich community of plugin developers.

[https://grafana.com/](https://grafana.com/)

Other clients are in development as well, including a command line tool for basic management, a curses based monitoring tool for easy testing over ssh, a Java based tool for graph generation, and a Tkinter based tool for graphical live monitoring and management.

## Future Goals

At the moment, SCADA is a strictly passive system in its relationship to the CAN bus. The services described above implement a pure data aquisition system which listens to the CAN bus and presents the incoming data to the user, but does not have the ability to talk on that bus to issue commands or configure the network for certain behaviors. This means that SCADA is, by definition, incomplete. There needs to be a way to perform supervisory control functions by talking back to the network.

Because data aquisition is the most important part of the FSAE team's need for a SCADA system, these were the services that were built first, but more work is required to turn this into a complete SCADA system. In addition, the SCADA PI needs to perform some secondary services that are not strictly part of the SCADA system. An example of a more complete SCADA design that includes non-implemented features is shown below.

![](https://raw.githubusercontent.com/Lafayette-FSAE/scada/master/diagrams/planned-final-design.svg)

A list of the additional services depicted and a description of their function is included below:

### Instruction Parser

The instruction parser would serve as a counterpart to the sorter. Instead of reading from the CAN bus, it would write to it, and serve as the bridge through which the rest of SCADA could send control signals to the car's other subsystems.In order to keep the other SCADA services agnostic about exact CAN message syntax, a text based format should be agreed upon for representing control signals that can sent over the CAN network. The instruction parser would then have the sole responsibility of parsing this format into CAN messages.

### Watcher

The instruction parser would, by default, receive most of its instructionss from client programs, which would in turn receive instructions from the User, who would make decisions about which comands to send by viewing the incoming data. This forms a feedback loop for doing certain kinds manual system control. However, there will most likely be a need for an additional, automatic feedback loop which can take place at a higher frequency and without user intervention.

In theory, a client could be written to perform such a task, but it would not continue to run after it was disconnected. Instead, a dedicated service should be written, which regularly polls the Redis server for the state of the car, and makes decisions about what commands to send based on this data. It could be configured as a list of condition, instruction pairs, and would be useful for things like opening the safety loop during emergency conditions.

### GLV-CAN Interface

The GLV board contains a number of sensors and control vectors that should ideally be exposed to the rest of the car using the standard CANOpen interface. This could, in theory, be done by a dedicated microcontroller, like is done with the car's other subsystems, but the proximity of the SCADA Pi to these sensors has meant that, for better or for worse, it has absorbed these responsibilities. 

Nevertheless, the GLV-CAN interface should be thought of as distinct from SCADA, and written as its own program that only interfaces with SCADA through the CAN bus. This has the drawback of requiring some extra steps in the communication process, but it allows other nodes on the network to access data from the GLV system. In addition, it helps to keep SCADA implementation more "pure" in the sense that it does not require the need for built in exceptions and special behavior based on the method the data was obtained. Previous implementations of SCADA were riddled with such exceptions, and they were a common source of complaints.

### Subsystem Emulators

In the absence of a fully integrated system, testing the CAN interface of a given subsystem can be a difficult task. For example, you may want one of the batteries to behave differently based on the state of the other one, but only have constructed a single prototype. The DashMan system may want to test the way it responds to a certain TSI state, but the last TSI board may have been fried do to a wiring error. And of course, you may be forced by unforseen circumstances to develop SCADA and all other subsystems remotely and while forbidden to come within six feet of the lab, the car, or eachother.

For such events, the 2020 team has begun work on a series of Subsystem Emulators, which are meant to be run either on the SCADA Pi or a separate CAN connected computer, and mimic the CAN interface of each subsystem. Each emulator should mimic its subsystems's Object Dictionay, SDO server, and Transmit PDO messages. While not necessary, additional hardware like LEDs and buzzers would also be fun. 

### Extra Ideas

**SDOs**

The instruction parser would also be required for reading SDO data from the network. This is because the SDO operates on the client server communication model, rather than the producer consumer model used by PDO data.  

# How to Use

## Installation

### Prerequisites

SCADA assumes it is being run on a debian based linux distribution. This will almost always be raspbian, but it has also been tested on a pure debian server. This should also work on something like ubuntu, but this has not been tested. SCADA will not work on a Windows or Mac, and most likely never will. This is by design, as SCADA takes advantage of a large number of assumptions about its environment. 

It is recommended to set up a dedicated development server for SCADA using a spare raspberry pi and ideally something resembling the GLV hardware. This could be expanded over time into include a mock CAN bus for integration testing with other subsystems.

Because the Lafayette network can be difficult to navigate, it is recommended that this be bypassed using either a dedicated physical network or vpn. This could be set up in such a way as to prevent ip address changes and to enable offsite work.

### Install Script

One of the drawbacks of the small and modular approach to system development is that installation becomes a bit more tricky. To help mitigate this, an install script is included with SCADA which is meant to help automate the process.

Ideally, a full installation of SCADA could be performed with the following shell commands:

```bash
$ git clone https://github.com/Lafayette-FSAE/scada
$ cd scada
$ sudo bash install
```

However, becasue SCADA is still relatively new software, the install script is likely to fail in some environments, requireing manual intervention. In addition, updates will need to be made to the install script periodically as new features are added to SCADA. To that end, an explanation of the install script and what it does is provided here.


```bash
apt-get install python3
apt-get install python3-pip
apt-get install redis-server
apt-get install can-utils
```

This section uses apt-get to install 3rd party programs and dependencies. New dependencies can be added to SCADA by appending apt-get calls to this list.

```bash
# install python dependencies
pip3 install python-can
pip3 install redis
pip3 install blessed
pip3 install psycopg2-binary
```

Next, the python package manager is used to install python specific dependencies.

```bash
# make sure virtual can bus is set up for testing
modprobe vcan
ip link add dev vcan0 type vcan
ip link set up vcan0
```

The Pi's CAN interface is created and turned on. This is currently configured to use a virtual CAN interface for development and testing, but can be switched to the real CAN bus by replacing all instances of vcan with can.

```bash
# make binary files executable
chmod +x install
chmod +x scada
chmod +x sorter/sorter.py
chmod +x calibrator/calibrator.py
chmod +x logger/logger.py
```

Files which need to be executable are made so explicitly with the chmod command. This includes scripts which are run as services, the scada cli interface and this install script.

```bash
# copy binary files to /usr/bin
cp scada /usr/bin/scada
cp sorter/sorter.py /usr/bin/scada_sorter.py
cp calibrator/calibrator.py /usr/bin/scada_calibrator.py
cp logger/logger.py /usr/bin/scada_logger.py
```

Copy executable files into a known directory. The exact directory chosen is sort of arbitrary, so long as it matches the directory written in the .service files. /usr/bin is a good choice because it is the standard for user installed binary files and it is already in the PATH variable. 

```bash
# create a workspace and copy important files into it
mkdir -p /usr/etc/scada
rm -rf /usr/etc/scada/utils
cp -r utils /usr/etc/scada/utils
rm -rf /usr/etc/scada/config
cp -r config /usr/etc/scada/config
cp ./install /usr/etc/scada
```

This also copies files into a known directory, this time the non executable files, and to the /usr/etc/scada directory. Again this was chosen arbitrarily. This is where the services will look for things like custom python libraries and config files.

```bash
# copy service files for systemd
cp sorter/sorter.service /etc/systemd/system
cp calibrator/calibrator.service /etc/systemd/system
cp logger/logger.service /etc/systemd/system
```

Finally copy the .service files into a place where systemd can find them. This directory is not arbitrary, and must be /etc/systemd/system

### Verification

TODO

## Configuration

While SCADA consists of several distinct programs, for the sake of convenience, they all read from the same set of configuration files. At the moment, there are two, both of which can be found in the config directory. 

`config.yaml` is a general purpose config file which handles the majority of options. `user_cal.py` is a python file specific to the calibrator which defines the calibration functions it will use to map data as it comes in. Together they make up the full set of configuration options for SCADA.

The following sections explain the configuration options in further detail.


### Bus Info

The bus info section gives the sorter information about the CAN bus. For the most part these options are passed directly

If you are running SCADA on a system without a CAN interface, set bustype to virtual.

Virtual CAN networking can also be acheived by using the vcan0 channel of socketcan.

As it is currently configured, the raspberry pi in the Dyno room talks to the rest of
the network on the can0 channel of socketcan with a bitrate of 125000

If bustype is set to virtual, channel and bitrate fields can be omitted

```yaml
bus_info:
  bustype: socketcan
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


### Calibration

Calibration is configured in a separate python file called `user_cal.py` in the calibration folder. A Calibration function is defined using the `@cal_function` function decorator, which takes two arguments:

- `output`: the name of the data being generated
- `arguments`: a list of the data needed as arguments

Because the calibrator operates only on data within the Redis cache, `output` and `arguments` should both contain Redis keys. These can be any string in theory, but, by convention, consist of all lower case characters, and are organized into heirarchies via the `:` character. (For example, all keys that store data about the TSI take the form `tsi:*`)

It is important that the keys written in the arguments list correspond to those those written in the data section of the `config.yaml` file. Otherwise, the sorter and calibrator will not agree on where to look for data. It is also important to ensure the output key does not conflict with any other input or output keys.

To help avoid key collisions, when multiple keys are used to represent the same piece of data, but transformed in some way, such as in the case of a linear calibration or unit conversion, they should be distinguished from eachother with the use of a second `:` followed by a modifier. Only the key that is meant to represent the default form of the data should omit this modifier. The grouping of keys in this way allows for easier querying of the available data by downstream programs. For example, in the case of the TSI, data is transmitted as raw sensor values, and converted into usable units by calibration functions. The non calibrated data is stored with the key `tsi:<data>:raw` and its converted form is stored under `tsi:<data>`.

#### Examples

**1. celcius to farenheit**

 ```python
# Converts ambient temp of pack1 to farenheit because
# we live in America god damn it
@cal_function(output='pack1:temp:farenheit', arguments=['pack1:temp'])
def packtemp_farenheit(args):
	temp, *other = args
	temp_faranheit = temp * (9/5) + 32
	return temp_faranheit
```

**2. voltage and current to power**

 ```python
# Calculates the TS power draw in kW
@cal_function(output='tsi:power', arguments=['tsi:voltage', 'tsi:current'])
def ts_power(args):
	voltage, current, *other = args
	power = (voltage * current) / 100
	return power
```


**3. motor controller voltage from sensor data**

```python
@cal_function(output='tsi:mc_voltage', arguments=['tsi:mc_voltage:raw'])
def mc_voltage(args):
	mc_voltage_raw, *other = args
	return (((mc_voltage_raw / 255) * 5) - 1.28) * 61
```

**4. TSI state enumeration**

```python
@cal_function(output='tsi:state', arguments=['tsi:state:int'])
def state(args):
	state_number, *other = args

	if state_number == 1:
		return 'GLV-ON'
	elif state_number == 2:
		return 'AIRS-CLOSED'
	elif state_number == 3:
		return 'DRIVE SETUP'
	elif state_number == 4:
		return 'READY TO DRIVE SOUND'
	elif state_number == 5:
		return 'DRIVE'
	else:
		return 'STATE UNDEFINED'
```

**5. Motor Controller Throttle**

```python
@cal_function(output='motor:throttle', arguments=[
    'motor:throttle:byte0',
    'motor:throttle:byte1'
])
def throttle(args):
	lsb, msb, *other = args
	return msb * 256 + lsb
```

Data generated by these functions will be written to the same data cache structure as the rest, and will have an index determined by the `output` argument, allowing it to be accesed by other programs downstream.



## Viewing Data

### Setting up Grafana

# Extending SCADA
