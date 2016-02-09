#!/usr/bin/env python

from __future__ import print_function

import serial
import json
import time

def main():
    values = []
    with serial.Serial('/dev/tty.usbmodem1411', 9600) as port:
        line_read = []
        start_time = time.time()
        try:
            while True:
                last_data_read = port.read(5)
                for character in last_data_read:
                    if character == '\n':
                        value = int(''.join(line_read).strip())
                        values.append({
                            "value": value,
                            "time_offset": time.time() - start_time,
                        })
                        print(value)
                        line_read = []
                    else:
                        line_read.append(character)
        except KeyboardInterrupt:
            with open('data.json', 'w') as fh:
                json.dump(values, fh)


if __name__ == '__main__':
    main()
