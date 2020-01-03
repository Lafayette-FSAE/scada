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

```yaml
bus_info:
  bustype: socketcan | virtual
  channel: can0 | vcan0 | (or any other socketcan channel)
  bitrate: 125000
```

### Emulation

```yaml
emulate_nodes: yes

# enable specific node emulation
emulate_tsi: yes
emulate_packs: yes
emulate_cockpit: no
emulate_motorcontroller: no
```
