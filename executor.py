"""Simulated stand-in for the internal `executor` package.

The real package sends the command over HTTP to the robot's IP, blocks
until the robot replies, and raises if it can't reach the robot.
This simulation sleeps for a scaled-down duration per command and
randomly drops replies to mimic the flaky lab network.

(This file is "given" — it is NOT part of the code under review.)
"""

import random
import time

# Scaled-down durations (real ones: instant / few sec / ~30s / several minutes)
_DURATIONS = {
    "get_status": 0.1,
    "move_arm": 1.0,
    "walk": 3.0,
    "firmware_update": 6.0,
}

_DROP_RATE = 0.25  # chance the reply is lost on the way back


def execute(ip: str, command_string: str) -> str:
    if command_string not in _DURATIONS:
        raise ValueError(f"unknown command: {command_string!r}")
    time.sleep(_DURATIONS[command_string])
    if random.random() < _DROP_RATE:
        raise ConnectionError(f"lost reply from {ip} for {command_string!r}")
    return f"{command_string} done (reply from {ip})"
