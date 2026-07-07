#!/bin/bash

MAX_TEMP=80

TEMP=$(vcgencmd measure_temp | grep -o '[0-9.]*')

if (( $(echo "$TEMP >= $MAX_TEMP" | bc -l) )); then
    logger "MTA LED Matrix: Temperature ${TEMP}C exceeded ${MAX_TEMP}C. Shutting down."

    systemctl stop ledmatrix.service

    shutdown -h now
fi