#!/usr/bin/env python

from __future__ import print_function

import serial
import os
from birdy.twitter import UserClient

CONSUMER_KEY = 'gU90Ph9KvpUhWerI8u7Wei5rz'
CONSUMER_SECRET = os.environ['TWITTER_CONSUMER_SECRET']
ACCESS_TOKEN = '4889176491-swAd6fQDbLibzG4ule2tiYuuLA5Cob6eGvIVQdb'
ACCESS_TOKEN_SECRET = os.environ['TWITTER_ACCESS_TOKEN_SECRET']

twitter_client = UserClient(CONSUMER_KEY,
                    CONSUMER_SECRET,
                    ACCESS_TOKEN,
                    ACCESS_TOKEN_SECRET)


THRESHOLD = 900

def main():
    recent_values = []
    with serial.Serial('/dev/tty.usbmodem1411', 9600) as port:
        line_read = []
        while True:
            last_data_read = port.read(10)
            for character in last_data_read:
                if character == '\n':
                    value_line = ''.join(line_read)
                    value = int(value_line.split('=')[1].strip())
                    # recent_values.append(value)
                    if value > THRESHOLD:
                        twitter_client.api.statuses.update.post(status='I just flexed %d JIGGAWATTS!' % value)
                        print('Tweeted!')

                    print(value_line)
                    line_read = []
                else:
                    line_read.append(character)



if __name__ == '__main__':
    main()
