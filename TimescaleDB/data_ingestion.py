from mqtt import connect_mqtt
import db_utils as utils
import models
import random
import json

BROKER = "mqtt.javos.dev"
PORT = 1883
client_id = f'python-mqtt-{random.randint(0, 1000)}'
username = ""
password = ""

def process_payload(topic:str, payload: str):
    data = json.loads(payload)

    topic_parts = topic.split('/')

    lab_id = topic_parts[0]
    device_id = topic_parts[1]
    device_port = topic_parts[2]

    lab = utils.get_or_create_lab(lab_id, lab_id)
    device = utils.get_or_create_device(lab.id, device_id, device_port)

    for measure in data:
        try:
            measurement = utils.get_or_create_measurement(measure, measure, None, type(data[measure]) == str)
            value = data[measure]
            if type(value) == str:
                string_map = utils.get_or_create_string(measurement_id=measurement.id, string=value)
                value = string_map.value
            
            saved_value = utils.create_value(lab_id=lab.id, device_id=device.id, measurement_id=measurement.id, value=value)
            print(f"Saved value: {saved_value.id if saved_value != None else -1}")
        except Exception as e:
            pass
            # print("ERROR in process_payload:")
            # print(topic)
            # print(measure, data[measure])

def process_mqtt_message(client, userdata, message):
    topic = message.topic
    try:
        payload = message.payload.decode()
        print(f"Received message from `{topic}` topic. Processing...")
        if len(topic.split('/')) == 3:
            process_payload(topic, payload)
        else:
            print("Invalid topic. Skipping...")
            print(f"Payload: {payload}")
    except Exception as e:
        print("ERROR in process_mqtt_message:")
        print(e)
        print(topic)

def run():
    client = connect_mqtt(BROKER, PORT, client_id, username, password)
    client.on_message = process_mqtt_message
    client.subscribe("#")
    client.loop_forever()

if __name__ == '__main__':
    run()
