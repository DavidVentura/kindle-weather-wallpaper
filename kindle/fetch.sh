#!/bin/bash
SERVER="http://web.labs/tmp.png"
FILE="/mnt/us/tmp.png"
HEADER=""
HEADER="Host: weather.davidventura.com.ar"

wget --header="$HEADER" -O "$FILE" "$SERVER"


if [ $? -eq 0 ]; then
	eips -f -g "$FILE"
fi
