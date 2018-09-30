#!/bin/bash
ntpd -q -g
cd /home/pi/
source env/bin/activate
export PYTHONPATH="${PYTHONPATH}:/usr/local/lib/python3.5/dist-packages"
export PYTHONPATH="${PYTHONPATH}:/usr/local/lib/python3.5/dist-packages/rpi_ws281x-1.0.0-py3.5-linux-armv7l.egg"
cd /home/pi/assistant/
python3 -m shineon &