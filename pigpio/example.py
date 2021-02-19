from __future__ import print_function
import time
from drv8835_driver_pigpio import motors, MAX_SPEED, cleanup

# Set up sequences of motor speeds.
test_forward_speeds = list(range(0, MAX_SPEED, 2000)) + \
  [MAX_SPEED] * 200 + list(range(MAX_SPEED, 0, -2000)) + [0]  

test_reverse_speeds = list(range(0, -MAX_SPEED, -2000)) + \
  [-MAX_SPEED] * 200 + list(range(-MAX_SPEED, 0, 2000)) + [0]  

try:
    motors.setSpeeds(0, 0)

    print("Motor 1 forward")
    for s in test_forward_speeds:
        motors.motor1.setSpeed(s)
        time.sleep(0.005)

    print("Motor 1 reverse")
    for s in test_reverse_speeds:
        motors.motor1.setSpeed(s)
        time.sleep(0.005)

    print("Motor 2 forward")
    for s in test_forward_speeds:
        motors.motor2.setSpeed(s)
        time.sleep(0.005)

    print("Motor 2 reverse")
    for s in test_reverse_speeds:
        motors.motor2.setSpeed(s)
        time.sleep(0.005)

finally:
  # Stop the motors, even if there is an exception
  # or the user presses Ctrl+C to kill the process.
  motors.setSpeeds(0, 0)
  cleanup()

