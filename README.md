# drv8835-motor-driver-pigpio-python

Python library for the Pololu DRV8835 dual motor driver kit for Raspberry Pi using the [pigpio](http://abyz.me.uk/rpi/pigpio/) daemon

This repo contains versions of [Pololu's driver](https://github.com/pololu/drv8835-motor-driver-rpi) for their [DRV8835 Dual Motor Driver Kit for Raspberry Pi](https://www.pololu.com/product/2753).

Unlike the Pololu driver there is no dependency on the deprecated [wiringPi](http://wiringpi.com/) library. Instead this library utilizes the [pigpio](http://abyz.me.uk/rpi/pigpio/) daemon (```pigpiod```) and uses a Python client library to communicate with the daemon.

Two versions of the driver are provided using different underlying Python client libraries to communicate with ```pigpiod```:

- A standard (blocking) socket I/O via the official [```pigpio``` Python client library](http://abyz.me.uk/rpi/pigpio/python.html) (supports Python 2.x and 3.x).
- An [asyncio](https://docs.python.org/3/library/asyncio.html) based version using the unofficial (and still incomplete) [apigpio](https://github.com/neildavis/apigpio) library (Python3.7+ required).

## A note on hardware PWM support

This library uses the [```http://abyz.me.uk/rpi/pigpio/python.html#hardware_PWM```](http://abyz.me.uk/rpi/pigpio/python.html#hardware_PWM) API in ```pigpio``` to make use of true hardware PWN on pins 12 & 13 of the Pi. This generates 250 KHz PWM, which is the maximum supported by the Pololu DRV8835 chip.

## Getting Started

### Installation

First, ensure you have the pigpio dameon installed:

```bash
sudo apt-get install pigpio
```

### Starting the pigpiod daemon

This library uses a Python *client library* which in turn communicates with the pigpio dameon process which must be running, otherwise your program will receive an error. To start the daemon you can type:

```bash
sudo gpiod
```

See also discussion above regarding passing a PWM *sample rate* via the ```-s``` parameter when starting the daemon if you require a frequency above 5KHz.

### Stopping the pigpiod daemon

When you're done you can stop the daemon if you want by typing:

```bash
sudo killall pigpiod
```

### Using the library

Specific instructions for using the [pigpio Python client library](http://abyz.me.uk/rpi/pigpio/python.html) based version of this library can be found in the [README](pigpio/README.md) file in the ```pigpio``` directory.

If you prefer to use an [asyncio](https://docs.python.org/3/library/asyncio.html) based version of the Python client library, a version of the library using [apigpio](https://github.com/neildavis/apigpio) is available in the ```apigpio``` directory. See the [README](apigpio/README.md) in that directory for specific instructions in this case. Note this version is limited to use with Python 3.7+
