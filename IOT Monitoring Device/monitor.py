from loguru import logger
from mate3.api import Mate3Client
from mate3.api import DeviceValues
from mate3.field_values import FieldValue
from mqtt import connect_mqtt, publish

import json, dataclasses
from datetime import datetime
from asyncio import run

from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.interval import IntervalTrigger

def list_devices(devices: DeviceValues) -> dict:
    
    names = devices.__dict__.keys()

    actual_devices = {}

    for name in names:
        device = getattr(devices, name)
        if type(device) == dict and len(device) > 0:
            logger.info(f"Found device {name} with {device.keys()} ports")
            actual_devices[name] = list(device.keys())

    return actual_devices

def list_variables(devices: DeviceValues, device_name: str, port: int):

    variables = {}
        
    device = getattr(devices, device_name)
    if type(device) == dict and len(device) > 0:
        device = device[port]
        variables = device.__dict__.keys()

    return variables

def read_variable(devices: DeviceValues, device_name: str, port: int, variable: str):

    device = getattr(devices, device_name)
    if type(device) == dict and len(device) > 0:
        device = device[port]
        variable = getattr(device, variable)
        if type(variable) == FieldValue:
            variable.read()
            return variable.value

class JSONEncoder(json.JSONEncoder):
        def default(self, o):
            if dataclasses.is_dataclass(o):
                return dataclasses.asdict(o)
            try:
                return super().default(o)
            except TypeError:
                return str(o)

def read_and_send_variables(mate_client: Mate3Client, mqtt_client):
    devices = list_devices(mate_client.devices)

    mqtt_client.publish(f"kiosol/last_date", datetime.now().isoformat())

    for device_name in devices:
        for port in devices[device_name]:
            variables = list_variables(mate_client.devices, device_name, port)
            values = {}
            for variable in variables:
                try:
                    values[variable] = read_variable(mate_client.devices, device_name, port, variable)
                except Exception as e:
                    pass

            mqtt_client.publish(f"kiosol/{device_name}/{port}", json.dumps(values, cls=JSONEncoder))

            logger.info(f"{device_name} {port} Values Sent for {len(values)} variables")

def read_and_send_variable(mate_client: Mate3Client, mqtt_client, device_name, port, variable):
    value = read_variable(mate_client.devices, device_name, port, variable)
    mqtt_client.publish(f"kiosol/{device_name}/{port}/{variable}", json.dumps(value, cls=JSONEncoder))


def main():
    logger.remove()
    logger.add(sys.stderr, level="INFO")

    mqttClient = connect_mqtt(
        broker="157.253.242.156",
        port=1883,
        client_id="mate3",
        username="",
        password="",
    )

    scheduler = BlockingScheduler()
    
    def change_measure_interval(client, userdata, message):
        logger.info(f"Changing measure interval to {message.payload}")
        seconds = int(message.payload)
        if seconds < 1:
            scheduler.pause_job("measure")
            logger.info("Measure job paused")
        else:
            scheduler.reschedule_job("measure", trigger=IntervalTrigger(seconds=seconds))

    mqttClient.on_message = change_measure_interval

    mqttClient.subscribe("kiosol/measure_interval")
    mqttClient.loop_start()


    with Mate3Client(host="192.168.0.65") as client:

        # print(list_devices(client.devices))
        # print(list_variables(client.devices, "fndcs", 3))
        # print("")
        scheduler.add_job(
            read_and_send_variables,
            trigger=IntervalTrigger(seconds=30),
            id="measure",
            args=[client, mqttClient],
        )

        # scheduler.add_job(
        #     read_and_send_variable,
        #     trigger=IntervalTrigger(seconds=1),
        #     args=[client, mqttClient, "fndcs", 3, "battery_voltage"],
        # )

        scheduler.start()
        # read_and_send_variables(client, mqttClient)

if __name__ == "__main__":
    import sys
    import time

    main()