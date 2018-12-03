var noble = require('noble');
const mqtt = require ('mqtt');

var options = {host:'192.168.43.129', port:1883};
var client = mqtt.connect(options);

client.on('connect', function() { // When connected
    console.log('connected');
});

const peripheralAddress = "30:ae:a4:1c:01:c2"; //esp32 address
//If name filtering is required
const peripheralName = "SeeCat07";
const sensorDataTopic = "deviceID/SeeCat07/sensorData";

noble.on('stateChange', function(state) {
  if (state === 'poweredOn') {
    noble.startScanning();
  } else {
    noble.stopScanning();
  }
});

noble.on('discover', function(peripheral) {
  if (peripheral.address === peripheralAddress) {
    noble.stopScanning();
    var deviceID = 0;
    const timeoutObj = setTimeout(() => {
	  console.log('WatchDog timeout hit beyond time');
    }, 20000);

    console.log('Sensor with ID ' + peripheral.id + ' found');
    var advertisement = peripheral.advertisement;

    var localName = advertisement.localName;
    var manufacturerData = advertisement.manufacturerData;

    if (localName) {
      console.log('SensorName        = ' + localName);
      deviceID = localName;
    }

    if (manufacturerData) {
	var readings = (advertisement.manufacturerData).slice(2, advertisement.manufacturerData.byteLength).toString('ascii').split(",");
	var sensordata = {
	    temperature: readings[0],
	    humidity: readings[1],
	    deviceId: deviceID
	}
	console.log(sensordata);

	if(deviceID !== 0) {
		client.publish(sensorDataTopic, JSON.stringify(sensordata));
		clearTimeout(timeoutObj);
	}
    }
    console.log();

    noble.startScanning();

  }
});
