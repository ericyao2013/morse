#! /usr/bin/env python
"""
This script tests the 'data stream' oriented feature of the socket interface.
"""

from morse.testing.testing import MorseTestCase

try:
    # Include this import to be able to use your test file as a regular 
    # builder script, ie, usable with: 'morse [run|exec] <your test>.py
    from morse.builder.morsebuilder import *
except ImportError:
    pass

import socket
import sys
import time
from pymorse import Morse


class BatteryTest(MorseTestCase):

    def setUpEnv(self):
        
        robot = Robot('atrv')

        battery = Sensor('battery')
        battery.configure_mw('socket')
        battery.properties(DischargingRate = 10.0)
        robot.append(battery)

        env = Environment('indoors-1/indoor-1')
        env.configure_service('socket')

    def test_read_battery(self):
        """ Test if we can connect to the pose data stream, and read from it.
        """

        with Morse() as morse:
            bat_stream = morse.stream('Battery')

            bat = bat_stream.get()
            cur_bat = bat['charge']
            time.sleep(2.0)

            bat = bat_stream.get()
            # Can't be really precise as we don't have exact timestamp
            # about when we get data
            self.assertAlmostEqual(bat['charge'] - cur_bat, -20.0, delta=0.5)
            cut_bat = bat['charge']

            # Now the battery must be empty
            time.sleep(10.0)
            bat = bat_stream.get()
            self.assertAlmostEqual(bat['charge'], 0.0, delta=0.001)



########################## Run these tests ##########################
if __name__ == "__main__":
    import unittest
    from morse.testing.testing import MorseTestRunner
    suite = unittest.TestLoader().loadTestsFromTestCase(BatteryTest)
    sys.exit(not MorseTestRunner().run(suite).wasSuccessful())
