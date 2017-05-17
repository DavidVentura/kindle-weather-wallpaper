#!/bin/bash
SERVER="http://web.labs/tmp.png"
FILE="/mnt/us/tmp.png"
HEADER=""
HEADER="Host: weather.davidventura.com.ar"


sleeping=$(lipc-get-prop com.lab126.powerd status | grep -c "Screen Saver")

if [ "$sleeping" -ne 1 ]; then
	echo "Not sleeping."
	exit 2
fi

wifienable() {
	lipc-set-prop com.lab126.cmd wirelessEnable 1
}

is_connected() {
	echo "$(lipc-get-prop com.lab126.wifid cmState | grep -c CONNECTED)";
}

wifienable
tries=0
while [ "$(is_connected)" -eq 0 ] && [ "$tries" -lt 10 ]; do
	echo 'sleeping for wifi...'
	tries=$((tries+1))
	sleep 1
done

if [ "$tries" -eq 10 ]; then
	echo "Wifi is off."
	exit 1
fi

echo 'wifi => Connected'
#wget --header="$HEADER" -O "$FILE" "$SERVER"
#Kindle's wget doesn't support --header
curl -s --header "$HEADER" "$SERVER" >"$FILE"                                   

if [ $? -ne 0 ]; then
	exit $?
fi


eips -f -g "$FILE"
