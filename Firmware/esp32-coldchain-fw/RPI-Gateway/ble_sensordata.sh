#!/bin/bash

while [ 1 ];
do
/etc/init.d/bluetooth restart
sleep 2
node ble_sensorclient.js
sleep 10
done
