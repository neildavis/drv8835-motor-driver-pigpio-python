# drv8835-motor-driver-pigpio-python
Python library for the Pololu DRV8835 dual motor driver kit for Raspberry Pi using the [pigpio](http://abyz.me.uk/rpi/pigpio/) daemon

This repo contains versions of [Pololu's driver](https://github.com/pololu/drv8835-motor-driver-rpi) for their [DRV8835 Dual Motor Driver Kit for Raspberry Pi](https://www.pololu.com/product/2753).

Unlike the Pololu driver there is no dependency on the deprecated [wiringPi](http://wiringpi.com/) library. Instead this library uses the [pigpio](http://abyz.me.uk/rpi/pigpio/) dameon and Python client library.

## A note on hardware PWM support
A consequence of using `pigpio` instead of `wiringPi` is that there is no *direct* support for the hardware PWM capabilities of the Pi on GPIO pins 12 & 13. PWM implemented in software usually incurs **significant CPU overhead**, and much **lower PWM frequencies** will typically be used (e.g. 3 KHz vs 20 KHz, i.e. non-ultrasonic).  However, mitigating this is the fact that `pigpio` runs as a [dameon](http://abyz.me.uk/rpi/pigpio/pigpiod.html) (one process regardless of number of clients using it) and also supports *hardware timing* for it's software PWM which is significantly more efficient than similar software only PWM implementations (e.g. [RPi.GPIO](https://pypi.org/project/RPi.GPIO/)). However this is still not *true hardware PWM* from the perspective of the Pi hardware's PWM functionality on pins 12 & 13, but it does have the benefit of PWM support being available on *all* GPIO pins.

This library requests 20&nbsp;kHz PWM from the pigpiod daemon to drive the motors. However the *actual* frequency achieved will depend on the parameters passed to the pigpiod daemon when it is started. See the documentation for [pigpiod -s](http://abyz.me.uk/rpi/pigpio/pigpiod.html) and also the table under [selectable frequencies](http://abyz.me.uk/rpi/pigpio/python.html#set_PWM_frequency) for your chosen sample rate parameter.

For example, if you start the pigpiod daemon without using a sample rate parameter (-s) parameter, the default of 5us will be used which limits the frequency to a maximum of 5KHz. To achieve 20Khz, the dameon needs to be started with the sample rate parameter (-s) of 1 or 2, e.g. ```sudo pigpiod -s 2```

## Getting Started

### Installation
First, ensure you have the pigpio dameon and python packages installed:
```bash
sudo apt-get install pigpio python-pigpio python3-pigpio
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

## TODO:
The [pigpio Python client library](http://abyz.me.uk/rpi/pigpio/python.html) uses blocking I/O for it's requests. Whilst this overhead is likely minimal for the GPIO output-only nature of this motor driver, it would be conveneient for Python3 developers making use of [apigpio](https://github.com/PierreRust/apigpio) for [asyncio](https://docs.python.org/3/library/asyncio.html) based GPIO monitoring etc, to not have to install a separate library. Support for this is planned.
