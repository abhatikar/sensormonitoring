var noble = require('noble');
const mqtt = require ('mqtt');

var options = {host:'192.168.43.129', port:1883, clean: true};
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


/*

function log(message, data) {
	  console.log(message + ' : ' + data)
}

noble.on('stateChange', function (data) { log('stateChange', data)});
noble.on('addressChange', function (data) { log('addressChange', data)});
noble.on('scanStart', function (data) { log('scanStart', data)});
noble.on('scanStop', function (data) { log('scanStop', data)});
noble.on('discover', function (data) { log('discover', data)});
noble.on('connect', function (data) { log('connect', data)});
noble.on('disconnect', function (data) { log('disconnect', data)});
noble.on('rssiUpdate', function (data) { log('rssiUpdate', data)});
noble.on('servicesDiscover', function (data) { log('servicesDiscover', data)});
noble.on('includedServicesDiscover', function (data) { log('includedServicesDiscover', data)});
noble.on('characteristicsDiscover', function (data) { log('characteristicsDiscover', data)});
noble.on('read', function (data) { log('read', data)});
noble.on('write', function (data) { log('write', data)});
noble.on('broadcast', function (data) { log('broadcast', data)});
noble.on('notify', function (data) { log('notify', data)});
noble.on('descriptorsDiscover', function (data) { log('descriptorsDiscover', data)});
noble.on('valueRead', function (data) { log('valueRead', data)});
noble.on('valueWrite', function (data) { log('valueWrite', data)});
noble.on('handleRead', function (data) { log('handleRead', data)});
noble.on('handleWrite', function (data) { log('handleWrite', data)});
noble.on('handleNotify', function (data) { log('handleNotify', data)});
*/

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
	    deviceId: deviceID,
	    timeStamp: Date.now()
	}
	console.log(sensordata);

	if(deviceID !== 0) {
		var pub_options = {
			qos:1
		};
		console.log('data published')
		client.publish(sensorDataTopic, JSON.stringify(sensordata), pub_options);
		clearTimeout(timeoutObj);
	}
    }

    console.log();

    noble.startScanning();
  }
});
