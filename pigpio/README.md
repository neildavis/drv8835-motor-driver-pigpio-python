# drv8835-motor-driver-pigpio-python

Python library for the Pololu DRV8835 dual motor driver kit for Raspberry Pi using the pigpio daemon and Python client API

## Summary

This library is a version of [Pololu's driver](https://github.com/pololu/drv8835-motor-driver-rpi) for their [DRV8835 Dual Motor Driver Kit for Raspberry Pi](https://www.pololu.com/product/2753). This library supports both Python 2 and Python 3 and aims to retain source compatibility so that it may be used as a *drop-in* replacement.

Unlike the Pololu driver there is no dependency on the deprecated [wiringPi](http://wiringpi.com/) library. Instead this library uses the [pigpio](http://abyz.me.uk/rpi/pigpio/) dameon and Python client library.

## Getting Started

### Installation

First ensure you have the pigpio dameon installed, and the ```pigpiod``` daemon running as descibed [here](../README.md)

Next, install the ```pigpio``` Python client library:

```bash
sudo apt-get install python-pigpio python3-pigpio
```

These instructions assume you will use Python 2. If you want to use Python 3, use the ```python3``` command instead of ```python``` for running Python scripts.

Next download and install this driver

```bash
git clone https://github.com/neildavis/drv8835-motor-driver-pigpio-python
cd drv8835-motor-driver-pigpio-python/pigpio
sudo python setup.py install
```

### Running the example program

This library comes with an example program that drives each motor in both directions.  To run the example, navigate to the `drv8835_driver_pigpio/pigpio` directory and run:

```bash
python example.py
```

## Library reference

In order to keep source compatibility with Pololu's driver API, absolute motor speeds in this library are represented as numbers between *-480* and *480* (inclusive).  Additional methods are provided to allow speed to be represented in percentage terms, i.e. as numbers between *-100* and *100* (inclusive).  A speed of 0 corresponds to braking.  Positive speeds correspond to current flowing from M1A/M2A to M1B/M2B, while negative speeds correspond to current flowing in the other direction.

The library can be imported into a Python program with the following line:

```python
from drv8835_driver_pigpio import motors, MAX_SPEED, cleanup
```

For convenience, a constant called ```MAX_SPEED``` (which is equal to 480) is available on all the objects provided by this library.  You can access it directly by just writing ```MAX_SPEED``` if you imported it as shown above, or it can be accessed in the following ways:

```python
motors.MAX_SPEED
motors.motor1.MAX_SPEED
motors.motor2.MAX_SPEED
```

After importing the library, you can use the commands below to set motor speeds in *absolute* terms (```-MAX_SPEED``` <= speed <= ```MAX_SPEED```):

```python
motors.setSpeeds(m1_speed, m2_speed) # Set speed and direction for both motor 1 and motor 2.
motors.motor1.setSpeed(speed) #Set speed and direction for motor 1.
motors.motor2.setSpeed(speed) #Set speed and direction for motor 2.
```

Alternatively, you can use the commands below to set the motor speeds in *percentage* terms (```-100``` <= speed <= ```100```):

```python
motors.setSpeedsPercent(m1_speed, m2_speed) # Set speed and direction for both motor 1 and motor 2.
motors.motor1.setSpeedPercent(speed) #Set speed and direction for motor 1.
motors.motor2.setSpeedPercent(speed) #Set speed and direction for motor 2.
```

When you are finished, before exiting your program call the library's `cleanup` function to ensure all GPIO resources are reset:

 ```python
 cleanup()
 ```

If you are controlling multiple motor drivers, you might prefer to import the library using:

 ```python
 import drv8835_driver_pigpio
 ```

 which requires the commands listed above to be prefixed with ```drv8835_driver_pigpio.```
