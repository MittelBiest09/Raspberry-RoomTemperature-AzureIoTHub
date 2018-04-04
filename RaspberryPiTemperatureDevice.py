import time
import sys
import iothub_client
from iothub_client import IoTHubClient, IoTHubClientError, IoTHubTransportProvider, IoTHubClientResult
from iothub_client import IoTHubMessage, IoTHubMessageDispositionResult, IoTHubError, DeviceMethodReturnValue
import os
import glob
import subprocess
import calendar
import time
import json

#initialize
os.system('modprobe w1-gpio')
os.system('modprobe w1-therm')

#device
base_dir = '/sys/bus/w1/devices/'
device_folder = glob.glob(base_dir + '28*')[0]
device_file = device_folder + '/w1_slave'

connectionData = json.load(open('connectionData.json'))
# String containing Hostname, Device Id & Device Key in the format
CONNECTION_STRING = connectionData["device_connection_string"]
DEVICE_ID = connectionData["device_id"]
# choose HTTP, AMQP or MQTT as transport protocol
PROTOCOL = IoTHubTransportProvider.MQTT
MESSAGE_TIMEOUT = 10000
SEND_CALLBACKS = 0
MSG_TXT = "{\"deviceId\": \"%s\",\"roomTemperature\": %.2f}"

def send_confirmation_callback(message, result, user_context):
    global SEND_CALLBACKS
    print ( "Confirmation[{0}] received for message with result = {1}".format(user_context, result))
    map_properties = message.properties()
    print ( "    message_id: {0}".format(message.message_id))
    print ( "    correlation_id: {0}".format(message.correlation_id))
    key_value_pair = map_properties.get_internals()
    print ( "    Properties: {0}".format(key_value_pair))
    SEND_CALLBACKS += 1
    print ( "    Total calls confirmed: {0}".format(SEND_CALLBACKS))

def iothub_client_init():
    # prepare iothub client
    client = IoTHubClient(CONNECTION_STRING, PROTOCOL)
    # set the time until a message times out
    client.set_option("messageTimeout", MESSAGE_TIMEOUT)
    client.set_option("logtrace", 0)
    client.set_option("product_info", "RaspberryPiTemperatureDevice")
    return client

def iothub_client_send_temperature():
    try:
        client = iothub_client_init()
        print ( "{0} sending periodic messages, press Ctrl-C to exit".format(DEVICE_ID) )
        message_counter = 0

        while True:
            msg_txt_formatted = MSG_TXT % (DEVICE_ID, read_temp())
            # messages can be encoded as string or bytearray
            if (message_counter & 1) == 1:
                message = IoTHubMessage(bytearray(msg_txt_formatted, 'utf8'))
            else:
                message = IoTHubMessage(msg_txt_formatted)
            # optional: assign ids
            message.message_id = "message_{0}".format(message_counter)
            message.correlation_id = "correlation_{0}".format(message_counter)
            # optional: assign properties
            prop_map = message.properties()
            prop_text = "PropMsg_{0}".format(message_counter)
            prop_map.add("Property", prop_text)

            client.send_event_async(message, send_confirmation_callback, message_counter)
            print ( "{0}.send_event_async accepted message [{1}] for transmission to IoT Hub.".format(DEVICE_ID, message_counter))

            status = client.get_send_status()
            print ( "Send status: {0}".format(status))
            time.sleep(30)

            status = client.get_send_status()
            print ( "Send status: {0}".format(status))

            message_counter += 1

    except IoTHubError as iothub_error:
        print ( "Unexpected error {0} from IoTHub".format(iothub_error))
        return
    except KeyboardInterrupt:
        print ( "{0} stopped".format(DEVICE_ID))

# Opens raw device, code changed to reflect issue in Raspian
def read_temp_raw():
    catdata = subprocess.Popen(['cat',device_file], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out,err = catdata.communicate()
    out_decode = out.decode('utf-8')
    lines = out_decode.split('\n')
    return lines

# Reads temperature, outputs farenhiet
def read_temp():
    lines = read_temp_raw()
    while lines[0].strip()[-3:] != 'YES':
        time.sleep(0.2)
        lines = read_temp_raw()
    equals_pos = lines[1].find('t=')
    if equals_pos != -1:
        temp_string = lines[1][equals_pos+2:]
        temp_c = float(temp_string) / 1000.0
        temp_f = temp_c * 9.0 / 5.0 + 32.0
        return temp_f

if __name__ == '__main__':
    print ( "Reading room temperature with Raspberry Pi and sending temperature to Azure IoT Hub" )
    print ( "    Protocol {0}".format(PROTOCOL))
    print ( "    Connection string={0}".format(CONNECTION_STRING))

    iothub_client_send_temperature()