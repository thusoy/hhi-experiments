#!/usr/bin/env python

from __future__ import print_function

import serial
import time
import json

def main():
    with open('data.json') as fh:
        values = json.load(fh)
    with serial.Serial('/dev/tty.usbmodem1411', 9600) as port:
        start_time = time.time()
        for value in values:
            while time.time() - start_time < value['time_offset']:
                pass
            port.write('%d\n' % value['value'])
            print('Wrote: %d' % (value['value'],))

if __name__ == '__main__':
    main()
