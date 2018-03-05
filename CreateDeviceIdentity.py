import sys
import iothub_service_client
from iothub_service_client import IoTHubRegistryManager, IoTHubRegistryManagerAuthMethod
from iothub_service_client import IoTHubDeviceStatus, IoTHubError
import json

connectionData = json.load(open('connectionData.json'))
CONNECTION_STRING = connectionData["connection_string"]
DEVICE_ID = connectionData["device_id"]

def print_device_info(title, iothub_device):
    print ( title + ":" )
    print ( "iothubDevice.deviceId                    = {0}".format(iothub_device.deviceId) )
    print ( "iothubDevice.primaryKey                  = {0}".format(iothub_device.primaryKey) )
    print ( "iothubDevice.secondaryKey                = {0}".format(iothub_device.secondaryKey) )
    print ( "iothubDevice.connectionState             = {0}".format(iothub_device.connectionState) )
    print ( "iothubDevice.status                      = {0}".format(iothub_device.status) )
    print ( "iothubDevice.lastActivityTime            = {0}".format(iothub_device.lastActivityTime) )
    print ( "iothubDevice.cloudToDeviceMessageCount   = {0}".format(iothub_device.cloudToDeviceMessageCount) )
    print ( "iothubDevice.isManaged                   = {0}".format(iothub_device.isManaged) )
    print ( "iothubDevice.authMethod                  = {0}".format(iothub_device.authMethod) )
    print ( "" )

def iothub_createdevice():
    try:
        iothub_registry_manager = IoTHubRegistryManager(CONNECTION_STRING)
        auth_method = IoTHubRegistryManagerAuthMethod.SHARED_PRIVATE_KEY
        new_device = iothub_registry_manager.create_device(DEVICE_ID, "", "", auth_method)
        print_device_info("CreateDevice", new_device)
        connectionData["device_connection_string"] = "HostName={0};DeviceId={1};SharedAccessKey={2}".format(connectionData["host_name"], new_device.deviceId, new_device.primaryKey)
        file = open('connectionData.json', 'w+')
        file.write(json.dumps(connectionData))
        file.close()

    except IoTHubError as iothub_error:
        print ( "Unexpected error {0}".format(iothub_error) )
        return
    except KeyboardInterrupt:
        print ( "iothub_createdevice stopped" )

if __name__ == '__main__':
    print ( "" )
    print ( "Python {0}".format(sys.version) )
    print ( "Creating device using the Azure IoT Hub Service SDK for Python" )
    print ( "" )
    print ( "    Connection string = {0}".format(CONNECTION_STRING) )
    print ( "    Device ID         = {0}".format(DEVICE_ID) )

    iothub_createdevice()