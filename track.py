#!/usr/bin/env python3
import time
import sys
import os
import signal

def save_pid(pid):
    with open("timer_pid.txt", "w") as file:
        file.write(str(pid))

def get_pid():
    try:
        with open("timer_pid.txt", "r") as file:
            return int(file.read().strip())
    except FileNotFoundError:
        return None

def countdown_timer(minutes) :
    seconds = minutes * 60
    while seconds:
        mins, secs = divmod(seconds, 60)
        timer_format = f"{mins:02d}:{secs:02d}"
        sys.stdout.write("\r" + timer_format)
        sys.stdout.flush()
        time.sleep(1)
        seconds -= 1
    print("\nTime's up!")
    for _ in range(3):
        sys.stdout.write('\a')
        sys.stdout.flush()

if __name__ == "__main__":
    try:
        minutes = 1
        print("Countdown timer started. Press Ctrl+z to put it in the background.")
        countdown_timer(minutes)
    except ValueError:
        print("Please enter a valid number of minutes.")
