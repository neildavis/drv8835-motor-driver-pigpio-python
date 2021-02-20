from distutils.core import setup
setup(name='drv8835_driver_apigpio',
      version='1.1.2',
      description=('Library for the Pololu DRV8835 Dual Motor '
                   'Driver Kit for Raspberry Pi using pigpio daemon with (asyncio based) apigpio client library'),
      url='http://www.pololu.com/product/2753',
      py_modules=['drv8835_driver_apigpio'],
      )
