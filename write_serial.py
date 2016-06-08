#!/usr/bin/env python

from __future__ import print_function

import serial
from birdy.twitter import StreamClient
import time
import os
import json

CONSUMER_KEY = 'EmwQewB82eqH0uBAObgRp1I4b'
CONSUMER_SECRET = os.environ['TWITTER_CONSUMER_SECRET']
ACCESS_TOKEN = '4889176491-6qwuvKfAHgxuQHqOV6Qpl2Axju4OtEaSMiTbd73'
ACCESS_TOKEN_SECRET = os.environ['TWITTER_ACCESS_TOKEN_SECRET']

twitter_client = StreamClient(CONSUMER_KEY,
                   CONSUMER_SECRET,
                   ACCESS_TOKEN,
                   ACCESS_TOKEN_SECRET)


def play_values(values, port):
    start_time = time.time()
    for value in values:
        while time.time() - start_time < value['time_offset']:
            pass
        port.write('%d\n' % value['value'])


def main():
    with open('data.json') as fh:
        values = json.load(fh)
    with serial.Serial('/dev/tty.usbmodem1411', 9600) as port:
        print('Got serial')
        response = twitter_client.stream.statuses.filter.post(track='#selfie')
        print('Listening to stream...')
        for data in response.stream():
            print('%s: %s' % (data['user']['screen_name'], data['text']))
            play_values(values, port)


if __name__ == '__main__':
    main()
