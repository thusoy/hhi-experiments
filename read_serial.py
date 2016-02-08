#!/usr/bin/env python

from __future__ import print_function

import serial
import os
import time
import sys
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
    name = get_name()
    print("Hello %s " % name)
    all_values = []
    with serial.Serial('/dev/tty.usbmodem1411', 9600) as port:
        line_read = []
        start_time = None
        has_started = False
        while not has_started or time.time() - start_time < 5:
            last_data_read = port.read(20)
            if not has_started:
                print("You have 5 seconds to flex. GO!")
                has_started = True
                start_time = time.time()
            for character in last_data_read:
                if character == '\n':
                    value_line = ''.join(line_read)
                    value = int(value_line.split('=')[1].strip())
                    all_values.append(value)
                    sys.stdout.write("\r%d  " % value)
                    sys.stdout.flush()
                    line_read = []
                else:
                    line_read.append(character)
        max_value = max(all_values)

        twitter_client.api.statuses.update.post(status='%s just flexed %d JIGGAWATTS!' % (name, max_value))
        print('\nGreat - you just flexed %d JIGGAWATTS' % max_value)


def get_name():
    return raw_input("Enter your name: ")



if __name__ == '__main__':
    main()
