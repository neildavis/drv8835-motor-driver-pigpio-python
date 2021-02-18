# drv8835-motor-driver-pigpio-python
Python library for the Pololu DRV8835 dual motor driver kit for Raspberry Pi using the pigpio daemon and Python client API

## Summary
This library is a version of [Pololu's driver](https://github.com/pololu/drv8835-motor-driver-rpi) for their [DRV8835 Dual Motor Driver Kit for Raspberry Pi](https://www.pololu.com/product/2753). This library supports both Python 2 and Python 3 and aims to retain source compatibility so that it may be used as a *drop-in* replacement.

Unlike the Pololu driver there is no dependency on the deprecated [wiringPi](http://wiringpi.com/) library. Instead this library uses the [pigpio](http://abyz.me.uk/rpi/pigpio/) dameon and Python client library.

### TODO:
The driver currently uses the [gpiod Python client library](http://abyz.me.uk/rpi/pigpio/python.html), which uses blocking I/O for it's requests. Whilst this overhead is likely minimal for the GPIO output-only nature of this motor driver, it would be conveneient for Python3 developers making use of [apigpio](https://github.com/PierreRust/apigpio) for [asyncio](https://docs.python.org/3/library/asyncio.html) based GPIO monitoring etc, to not have to install a separate library. Support for this is planned.

## A note on hardware PWM support
A consequence of using `pigpio` instead of `wiringPi` is that there is no *direct* support for the hardware PWM capabilities of the Pi on GPIO pins 12 & 13. PWM implemented in software usually incurs **significant CPU overhead**, and much **lower PWM frequencies** will typically be used (e.g. 3 KHz vs 20 KHz, i.e. non-ultrasonic).  However, mitigating this is the fact that `pigpio` runs as a [dameon](http://abyz.me.uk/rpi/pigpio/pigpiod.html) (one process regardless of number of clients using it) and also supports *hardware timing* for it's software PWM which is significantly more efficient than similar software only PWM implementation (e.g. [RPi.GPIO](https://pypi.org/project/RPi.GPIO/)). However this is still not *true hardware PWM* from the perspective of the Pi hardware's PWM functionality on pins 12 & 13, but it does have the benefit of PWM support being available on *all* GPIO pins.

This library requests 20&nbsp;kHz PWM from the pigpiod daemon to drive the motors. However the *actual* frquency will depend on the parameters passed to the pigpiod daemon when it is started. See the documentation for [pigpiod -s](http://abyz.me.uk/rpi/pigpio/pigpiod.html) and also the [frequencies available](http://abyz.me.uk/rpi/pigpio/python.html#set_PWM_frequency) for your chosen sample rate.

For example, if you start the pigpiod daemon without a sample rate parameter (-s) the default of 5ms will be used which limits the frequency to a maximum of 5KHz. To achieve 20Khz, the dameon needs to be started with the sample rate parameter of 1 or 2, e.g. ```sudo pigpiod -s 2```

## Getting Started

### Installation
These instructions assume you will use Python 2. If you want to use Python 3, use the ```python3``` command instead of ```python``` for running Python scripts.

First, ensure you have the pigpio dameon and python packages installed:
```bash
sudo apt-get install pigpio python-pigpio python3-pigpio
```

Next download and install this driver
```bash
git clone https://github.com/neildavis/drv8835-motor-driver-pigpio-python
cd drv8835-motor-driver-pigpio-python/pigpio
sudo python setup.py install
```

### Starting the pigpiod daemon
This library uses the pigpio Python *client library* which in turn communicates to the pigpio dameon process which must be running, otherwise your program will receive an error. To start the daemon you can type:
```bash
sudo gpiod
```
See also discussion above regarding passing a PWM *sample rate* via the ```-s``` parameter when starting the daemon if you require a frequency above 5KHz.

### Stopping the pigpiod daemon
When you're done you can stop the daemon if you want by typing:
```bash
sudo killall pigpiod
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

 