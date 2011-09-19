#!/usr/bin/env python
# Lucas Doyle wrote this

import subprocess
import string
import sys
import math
import os
import time

def beep(frequency, delay, length):
    p = subprocess.Popen(['beep', '-f', str(frequency), '-d', str(delay), '-l', str(length)], stdout=subprocess.PIPE)
    return

def main():
    
    a = 30;  # "stretch" factor for sin and cosine
    t = 0;    # time value
    
    while (a < 50) :
        t+=1
        if (t % 4 == 0) : a+=.02
        beep(2500 + a * math.degrees(math.sin(math.radians(t))), 1, 1)
        time.sleep(.0001 + (.001*a - (a*.002 - .001*a)))
        
    for a in range(10000):
        beep(a, 10, 10)
if __name__ == "__main__":
    main()


