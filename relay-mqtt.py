import paho.mqtt.client as mqttClient
import json
import wiringpi
import inc.board as board
from typing import List

hostname = '127.0.0.1'
topic = "mytopic"
hassTopicPrefix = "homeassistant/switch/thing"
friendlyNamePrefix = "Thing "
indexPayload = "things"
uniqueIdPrefix = "thing_"
icon = "mdi:power"


def set_relay(index, output, client: mqttClient.Client = None):
    board.updateRelay(index, output)
    if client != None:
        stateUrl = "{}{}/state".format(hassTopicPrefix, index)
        currentState = "ON" if output == board.HIGH else "OFF"
        client.publish(stateUrl, currentState, retain=True)
        print("published status update ", stateUrl, currentState, sep=' - ')


def set_relays(indexes, output, client: mqttClient.Client = None):
    for i in indexes:
        set_relay(i, output, client)


def set_relays_exclusive(indexes: List[int], output, client: mqttClient.Client = None):
    for i in range(len(board.relays)):
        if i in indexes:
            set_relay(i, output, client)
        else:
            set_relay(i, board.HIGH if output ==
                      board.LOW else board.LOW, client)


def on_message(client, userdata, msg):
    print("message received, parsing:", msg.payload)
    payload = json.loads(msg.payload.decode())
    cmd = payload["cmd"]
    affectedRelays = []
    if(indexPayload in payload):
        affectedRelays = payload[indexPayload]
    if cmd == "ON":
        print('turning on relays: ', affectedRelays)
        set_relays(affectedRelays, board.HIGH, client)
    elif cmd == "OFF":
        print('turning off relays:', affectedRelays)
        set_relays(affectedRelays, board.LOW, client)
    elif cmd == "ON-ONLY":
        print('turning on only relays: ', affectedRelays)
        set_relays_exclusive(affectedRelays, board.HIGH, client)
    elif cmd == "OFF-ONLY":
        print('turning off only relays:', affectedRelays)
        set_relays_exclusive(affectedRelays, board.LOW, client)
    elif cmd == "ON-ALL":
        print("turn ALL relays ON")
        set_relays(list(range(len(board.relays))), board.HIGH, client)
    elif cmd == "OFF-ALL":
        print("turn ALL relays OFF")
        set_relays(list(range(len(board.relays))), board.LOW, client)
    else:
        print("Unknown command, doing nothing")


def on_connect(client, userdata, flags, rc):
    print("Connection returned result: " + str(rc))
    client.subscribe(topic)
    if rc == 0:
        for index in range(0, len(board.relays)):
            discoveryUrl = "{}{}/config".format(hassTopicPrefix, index)
            pl_on = dict(cmd="ON")
            pl_on[indexPayload] = [index]

            pl_off = dict(cmd="OFF")
            pl_off[indexPayload] = [index]
            config = dict(
                name="{} {}".format(friendlyNamePrefix, index + 1),
                cmd_t=topic,
                pl_on=json.dumps(pl_on),
                pl_off=json.dumps(pl_off),
                stat_t="{}{}/state".format(hassTopicPrefix, index),
                icon=icon,
                optimistic=False,
                uniq_id="{}{}".format(uniqueIdPrefix, index),
                stat_on="ON",
                stat_off="OFF")

            config_string = json.dumps(config)
            print(config_string)
            client.publish(discoveryUrl, config_string, retain=True)


def on_log(client, userdata, level, buf):
    print("log: ", buf)


board.initialize()

# Connect to MQTT
currentClient = mqttClient.Client()
currentClient.on_message = on_message
currentClient.on_connect = on_connect
currentClient.on_log = on_log
currentClient.connect(hostname)
currentClient.loop_forever()
