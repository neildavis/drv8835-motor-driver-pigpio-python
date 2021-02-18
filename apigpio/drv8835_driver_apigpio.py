import asyncio
try:
    import apigpio 
except RuntimeError:
    print("Error importing pigpio module! Please ensure pigpio and python[3]-pigpio are installed")

# To keep source compatibility with Pololu's library using wiringPi we keep the range as -480 to 480
# Motor speeds for this library are specified as numbers
# between -MAX_SPEED and MAX_SPEED, inclusive.
_max_speed = 480
MAX_SPEED = _max_speed

# Default GPIO pin assignments
MOTOR1_PWM_PIN = 12
MOTOR1_DIR_PIN = 5
MOTOR2_PWM_PIN = 13
MOTOR2_DIR_PIN = 6
# Default PWM frequency - Since pigpio uses hardware timing we can go quite high
PWM_FREQUENCY=20000 # Up to 20 KHz, but actually depends on pigpio dameon start. See pigpiod -s
# Default host and port - Local on default port 8888
DEFAULT_HOST="127.0.0.1"
DEFAULT_PORT=8888

# Global pigpio pi object
the_pi = None

async def io_init(loop=asyncio.get_running_loop(), host=DEFAULT_HOST, port=DEFAULT_PORT):
    """GPIO initializer - global as done once regardless of number of instances of Motor/Motors classes"""
    global the_pi
    if not the_pi == None:
        return

    # Connect to the pigpio daemon
    the_pi=apigpio.Pi(loop)
    await the_pi.connect((host, port))
    # Setup GPIO modes & PWM params
    asyncio.gather(
        the_pi.set_mode(MOTOR1_PWM_PIN, apigpio.OUTPUT),
        the_pi.set_mode(MOTOR1_DIR_PIN, apigpio.OUTPUT),
        the_pi.set_mode(MOTOR2_PWM_PIN, apigpio.OUTPUT),
        the_pi.set_mode(MOTOR2_DIR_PIN, apigpio.OUTPUT),
        the_pi.set_PWM_frequency(MOTOR1_PWM_PIN, PWM_FREQUENCY),
        the_pi.set_PWM_range(MOTOR1_PWM_PIN, MAX_SPEED),
        the_pi.set_PWM_frequency(MOTOR2_PWM_PIN, PWM_FREQUENCY),
        the_pi.set_PWM_range(MOTOR2_PWM_PIN, MAX_SPEED)
    )
    asyncio.gather(
        # Set initial speed to 0 (stopped)
        the_pi.set_PWM_dutycycle(MOTOR1_PWM_PIN, 0),
        the_pi.set_PWM_dutycycle(MOTOR1_PWM_PIN, 0)
    )
 
async def cleanup():
    """Global cleanup"""
    global the_pi
    await the_pi.stop()

class Motor(object):
    MAX_SPEED = _max_speed

    def __init__(self, pwm_pin, dir_pin, pi):
        self.pwm_pin = pwm_pin
        self.dir_pin = dir_pin
        self.pi = pi

    async def setSpeed(self, speed):
        dir_value = 0
        if speed < 0:
            speed = -speed
            dir_value = 1
        if speed > MAX_SPEED:
            speed = MAX_SPEED
        await io_init()
        asyncio.gather(
            self.pi.set_PWM_dutycycle(self.pwm_pin, speed),
            self.pi.write(self.dir_pin, dir_value)
        )
 
    async def setSpeedPercent(self, speed):
        if speed < -100:
            speed = -100
        elif speed > 100:
            speed = 100
        # Map to range
        speed = speed * MAX_SPEED / 100
        await self.setSpeed(speed)
 
class Motors(object):
    MAX_SPEED = _max_speed

    def __init__(self):
        global the_pi
        self.motor1 = Motor(pwm_pin=MOTOR1_PWM_PIN, dir_pin=MOTOR1_DIR_PIN, pi=the_pi)
        self.motor2 = Motor(pwm_pin=MOTOR2_PWM_PIN, dir_pin=MOTOR2_DIR_PIN, pi=the_pi)

    async def setSpeeds(self, m1_speed, m2_speed):
        await io_init()
        await asyncio.gather(
            self.motor1.setSpeed(m1_speed),
            self.motor2.setSpeed(m2_speed)
        )

    async def setSpeedsPercent(self, m1_speed, m2_speed):
        await io_init()
        await asyncio.gather(
            self.motor1.setSpeedPercent(m1_speed),
            self.motor2.setSpeedPercent(m2_speed)
        )

motors = Motors()