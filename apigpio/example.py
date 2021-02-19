import asyncio
from drv8835_driver_apigpio import motors, MAX_SPEED, cleanup

async def main():
    # Set up sequences of motor speeds.
    test_forward_speeds = list(range(0, MAX_SPEED, 2000)) + [MAX_SPEED] * 200 + list(range(MAX_SPEED, 0, -2000)) + [0]  
    test_reverse_speeds = list(range(0, -MAX_SPEED, -2000)) + [-MAX_SPEED] * 200 + list(range(-MAX_SPEED, 0, 2000)) + [0]  

    try:
        await motors.setSpeeds(0, 0)

        print("Motor 1 forward")
        for s in test_forward_speeds:
            await motors.motor1.setSpeed(s)
            await asyncio.sleep(0.005)

        print("Motor 1 reverse")
        for s in test_reverse_speeds:
            await motors.motor1.setSpeed(s)
            await asyncio.sleep(0.005)

        print("Motor 2 forward")
        for s in test_forward_speeds:
            await motors.motor2.setSpeed(s)
            await asyncio.sleep(0.005)

        print("Motor 2 reverse")
        for s in test_reverse_speeds:
            await motors.motor2.setSpeed(s)
            await asyncio.sleep(0.005)

    finally:
        # Stop the motors, even if there is an exception
        # or the user presses Ctrl+C to kill the process.
        await motors.setSpeeds(0, 0)
        await cleanup()

if __name__ == "__main__":
    asyncio.run(main())
