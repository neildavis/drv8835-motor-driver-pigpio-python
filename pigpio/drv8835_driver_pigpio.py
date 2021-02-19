try:
    import pigpio 
except RuntimeError:
    print("Error importing pigpio module! Please ensure pigpio and python[3]-pigpio are installed")

# Motor speeds for this library are specified as numbers
# between -MAX_SPEED and MAX_SPEED, inclusive.
_max_speed = 1000000
MAX_SPEED = _max_speed

# Default GPIO pin assignments
MOTOR1_PWM_PIN = 12
MOTOR1_DIR_PIN = 5
MOTOR2_PWM_PIN = 13
MOTOR2_DIR_PIN = 6
# Default PWM frequency - Since pigpio uses hardware PWM we can go very high
PWM_FREQUENCY=250000 # 250 KHz is the max PWM supported by the 8835!
# Default host and port - Local on default port 8888
DEFAULT_HOST="127.0.0.1"
DEFAULT_PORT=8888

# Global pigpio pi object
the_pi = None

def io_init(host=DEFAULT_HOST, port=DEFAULT_PORT):
    """GPIO initializer - global as done once regardless of number of instances of Motor/Motors classes"""
    global the_pi
    if not the_pi == None:
        return

    # Connect to the pigpio daemon
    the_pi=pigpio.pi(host, port)
    # Setup GPIO modes & PWM params
    the_pi.set_mode(MOTOR1_DIR_PIN, pigpio.OUTPUT)
    the_pi.set_mode(MOTOR2_DIR_PIN, pigpio.OUTPUT)
     # Set initial PWM speeds to 0 (stopped)
    the_pi.hardware_PWM(MOTOR1_PWM_PIN, 0, 0)
    the_pi.hardware_PWM(MOTOR2_PWM_PIN, 0, 0)

def cleanup():
    """Global cleanup"""
    global the_pi
    the_pi.stop()

class Motor(object):
    MAX_SPEED = _max_speed

    def __init__(self, pwm_pin, dir_pin, pi):
        io_init()
        self.pwm_pin = pwm_pin
        self.dir_pin = dir_pin
        self.pi = pi

    def setSpeed(self, speed):
        dir_value = 0
        if speed < 0:
            speed = -speed
            dir_value = 1
        if speed > MAX_SPEED:
            speed = MAX_SPEED
        self.pi.hardware_PWM(self.pwm_pin, PWM_FREQUENCY, speed)
        self.pi.write(self.dir_pin, dir_value)

    def setSpeedPercent(self, speed):
        if speed < -100:
            speed = -100
        elif speed > 100:
            speed = 100
        # Map to range
        speed = speed * MAX_SPEED // 100
        self.setSpeed(speed)
 
class Motors(object):
    MAX_SPEED = _max_speed

    def __init__(self):
        io_init()
        global the_pi
        self.motor1 = Motor(pwm_pin=MOTOR1_PWM_PIN, dir_pin=MOTOR1_DIR_PIN, pi=the_pi)
        self.motor2 = Motor(pwm_pin=MOTOR2_PWM_PIN, dir_pin=MOTOR2_DIR_PIN, pi=the_pi)

    def setSpeeds(self, m1_speed, m2_speed):
        self.motor1.setSpeed(m1_speed)
        self.motor2.setSpeed(m2_speed)

    def setSpeedsPercent(self, m1_speed, m2_speed):
        self.motor1.setSpeedPercent(m1_speed)
        self.motor2.setSpeedPercent(m2_speed)

motors = Motors()
