#!/usr/bin/env python

from __future__ import print_function

from Quartz import CGEventPost, kCGSessionEventTap, CGEventCreateKeyboardEvent
import serial
import os
import time
import sys

KEYBOARD_TRESHOLD = 200

def press_space():
   sequence = [(49, True), (49, False)]
   for keycode, key_down in sequence:
       CGEventPost(kCGSessionEventTap, CGEventCreateKeyboardEvent(None, keycode, key_down))


def game():
    with serial.Serial('/dev/tty.usbmodem1411', 9600) as port:
        line_read = []
        last_event_at = time.time()
        while True:
            last_data_read = port.read(5)
            for character in last_data_read:
                if character == '\n':
                    value = int(''.join(line_read).strip())

                    if value >= KEYBOARD_TRESHOLD and time.time() - last_event_at > 0.3:
                        press_space()
                        last_event_at = time.time()

                    # sys.stdout.write("\r%d  " % value)
                    # sys.stdout.flush()
                    line_read = []
                else:
                    line_read.append(character)

def get_name():
    return raw_input("Enter your name: ")



if __name__ == '__main__':
    game()
