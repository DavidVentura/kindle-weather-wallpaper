#!/bin/bash
SERVER="http://web.labs/tmp.png"
FILE="/mnt/us/tmp.png "
wget -O "$FILE" "$SERVER"
if [ $? -eq 0 ]; then
	eips -f -g "$FILE"
fi
