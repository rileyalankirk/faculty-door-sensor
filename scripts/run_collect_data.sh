#!/bin/bash

cd /home/pi/faculty-door-sensor/
. .venv/bin/activate
cd src/FacultyDoorSensor/client_side
python3 collect_data.py