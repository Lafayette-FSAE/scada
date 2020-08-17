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

The most important thing to understand about the design of SCADA in its current form is that it is not a single program, but rather a system of programs which are made to run concurrently and interface with eachother. These programs try as much as possible to abide by the Unix Philosophy of software development, which is in essence, to write programs that are extremely limited in scope, and that interact well with each other. This is opposed to the way that SCADA has been written in the past, where a single large, integrated program is made to implement all the features required by the system. There are some drawbacks to the small and modular approach, which will be addressed later, but also a lot of advantages. They include the following:

- Features can usually be added without having to modify existing code, this can help to mitigate the square law of adding features to things.

- SCADA can be written in multiple different languages, so the best language can always be chosen for a given purpose, without having to make compromises.

- When the purpose of a program is general enough, existing open source software can be used instead of writing an in house solution.

- The individual components of the system are easy to understand and reason about.

- When problems arise, they are easy to isolate and diagnose. 

### Structure

SCADA Software in its current form is divided into the following services:

- A sorter
- A calibrator
- A logger
- A shared memory and communications bus (Redis)
- A database (Postgresql)
- A number of clients (Grafana, LARDAT, cli)

Wherever possible, general, open source tools are used instead of in house software.

Concurrency is handled by the operating system via systemd. All programs which are meant to be run as a service have an associated .service file, and can be managed with the systemctl interface.

[https://www.digitalocean.com/community/tutorials/how-to-use-systemctl-to-manage-systemd-services-and-units](https://www.digitalocean.com/community/tutorials/how-to-use-systemctl-to-manage-systemd-services-and-units)

For the most part, programs communicate with eachother via Redis. Redis is an open source in memory database that stores data as key value pairs, it also functions as a basic communications bus for sending simple inter-service messages.

[https://redis.io/](https://redis.io/)

If a program needs to write non-volitile data, it does so using an SQL database via a Postgres server. 

[https://www.postgresql.org/](https://www.postgresql.org/)

#### Data Aquisition

There are currently three in house services that deal with Data Aquisition. They are organized into a pipeline, with data being passed from one service to the next before eventually ending up in either the Redis or Postgres database  where it can be viewed by a client.

These services are, in order, the sorter, calibrator, and logger. Their responsibilities are as follows:

- **sorter**:
listens to the CAN bus for incoming messages, upon receiving a message, it checks its ID and Structure against a config file to generate an associated set of key value pairs. It then writes these key value pairs into the Redis cache and sends a message to the calibrator that new data has been received. The sorter is the only service that is aware of CAN or CANOpen, meaning SCADA can be made to work with a different networking protocol simply by switching out the sorter service for one made to work with the new protocol, without affecting any services downstream.

- **calibrator**:
The calibrator is responsible for translating the raw data read by the sorter from the CAN bus into a more human readable form. This is usually a case of linear calibration of raw sensor data, such as with the TSI node, or the recombining of data that was transmitted as multiple bytes, like with the Throttle value reported by Motor Controller. However, it can be made to support calculations of arbitrary complexity, such as for example, the calculation of power from a given voltage and current, the averaging of multiple sensors, filtering, differentiation, and so on. All calibrator operations are defined by the user as functions in the user_cal.py file. Once data is calculated, it is written back into the Redis server as a different key.

- **logger**:
The logger takes the data gathered by the sorter and calculated by the calibrator and logs a subset of it into the Postgresql database at regular intervals. The subset of data to be logged is defined in config.yaml file.

#### Clients

Both the Redis and Postgres servers expose TCP ports, and any software capable of interacting with these TCP ports can be considered a SCADA client. These clients can be run either locally on the SCADA Pi or remotely over a network. There are already a number of SCADA clients to choose from, and the best one for any given application will depend largely on circumstance and preference.

One potential 3rd party client that comes very highly recommended is Grafana. Grafana is an open source data viewing and monitoring tool that specializes in the construction of a wide range of data visualizations such as graphs, gauges, statistics, and logs based on a number of potential data sources. It supports Postgresql out of the box and is extremely easy to set up. It also has a rich community of plugin developers.

[https://grafana.com/](https://grafana.com/)

Other clients are in development as well, including a command line tool for basic management, a curses based monitoring tool for easy testing over ssh, a Java based tool for graph generation, and a Tkinter based tool for graphical live monitoring and management.

# How to Use

## Installation

One of the drawbacks of the small and modular approach to system development is that 

## Configuration

## Viewing Data

### Setting up Grafana

# Extending SCADA
