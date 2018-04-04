# Readme

This project contains a small python script to read temperature off a special sensor with your Raspberry Pi. The script will send the temperature data every few seconts to an Azure IoT Hub for further processing.
The following explains you which hardware and libraries you need to interact with your sensor and Azure IoT Hub.

# Hardware and set-up
## Hardware
 - Raspberry Pi (I'm using Raspberry Pi 3)
 - Breadboard
 - Temperature Sensor: As temperature sensor this project uses the DS18B20 Waterproof Digital temperature sensor, available on [Adafruit](https://www.adafruit.com/product/381)

## Set-up
Follow the instructions shown in [Jeremy Morgans blog](https://www.jeremymorgan.com/tutorials/raspberry-pi/monitor-room-temperature-raspberry-pi/) to wire up the sensor and test it.
As described in the tutorial, you have to install the following kernel modules:

    sudo modprobe w1-gpio 
    sudo modprobe w1-therm

# Azure IoT Hub

## Create device identity
As the script sends the measured temperature to an Azure IoT Hub, you have to create one first. To send your data to the Azure IoT Hub, you'll first have to create the DeviceIdentity on your Hub. This is done by the `CreateDeviceIdentity.py` script. Before executing the script you have to install the used python packages as described [here](https://github.com/Azure/azure-iot-sdk-python/blob/master/doc/python-devbox-setup.md). Install also the other used packages.
You are nearly there, but there is another thing to do. Create a `connectionData.json`which looks like the following:

    {
	    "host_name": "Azure IoT Hub name",
	    "connection_string": "Azure IoT Hub connection string",
	    "device_id": "RaspberryPiTemperatureDevice",
	    "device_connection_string": ""
	}

Get the `hostname` as well as the `connection_string` from creating your Azure IoT Hub. The script will fill the `device_connection_string` itself.
After executing the script now, you created a device identity for your Raspberry Pi to send the data to your Azure IoT Hub.

## Sending temperature data to Azure IoT Hub
To send your measured temperature data, you have to install the relevant Azure python packages as well as the other used python packages. Execute `RaspberryPiTemperatureDevice.py` to read your room temperature and send it to your Azure IoT Hub.

# Licence
MIT
