*Overview

This set of scripts is to allow communication from a Raspberry Pi to a SainSmart 16-relay board. 
It includes the plans for a custom board _(coming soon)_ that can be printed at any PCB distributor that will
bridge the Pi to the relay board without extra wiring.

**Dependencies**  
 - Python 3
 - MQTT
 - wiringpi

To run the script, simply replace the constants at the top of the `relay-mqtt.py` file and it should run as-is. Simply run the script or register it as a service _(documentation coming soon)_ and it will map an index to a relay number.

*MQTT commands

It should register itself for auto-discovery with homeassistant provided that has been enabled in homeassistant. It should include the configuration for telling homeassistant how to turn the relays on and off. For example, I've got mine set up to use a `home/speakers` topic, and I've replaced `thing` in the source-controlled version with `speaker`. Upon running, Homeassistant now has a "Speaker 1" with a unique ID of "speaker0" and turns it on/off at `home/speakers` by sending the payload: `{ "cmd": "ON", "speakers": [0] }`. Any time a relay is set, it will publish the simple string `ON` or `OFF` to a state topic.

**Other MQTT commands

There are other commands that can be used by sending other MQTT commands. They all take similar payloads. The most important differentiator is the `cmd` portion of the JSON payload.

 - `ON-ALL` - Turns on all relays
 - `OFF-ALL` - Turns off all relays
 - `ON-ONLY` - Turns on a given set of relays and turns any others off
 - `OFF-ONLY` - Turns off a given set of relays and turns any others on