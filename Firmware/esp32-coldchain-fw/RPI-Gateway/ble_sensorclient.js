var noble = require('noble');

const peripheralAdress = "30:ae:a4:20:14:aa";
//If name filtering is required
const peripheralName = "SeeCat03";

noble.on('stateChange', function (state) {
  console.log('on -> stateChange: ' + state);

  if (state === 'poweredOn') {
    noble.startScanning();
  } else {
    noble.stopScanning();
  }
});

noble.on('scanStart', function () {
  console.log('on -> scanStart');
});

noble.on('scanStop', function () {
  console.log('on -> scanStop');
})


noble.on('discover', function(peripheral) {
  if (peripheral.advertisement.localName == peripheralName || peripheral.address == peripheralAdress ) 
	{
	console.log(peripheral.address);
	console.log(peripheral.localName);
  peripheral.connect(function(error) {
    console.log('connected to peripheral: ' + peripheral.uuid);
    peripheral.discoverServices(['6e400001b5a3f393e0a9e50e24dcca9e'], function(error, services) {
    //peripheral.discoverServices(['180f'], function(error, services) {
      var batteryService = services[0];
      console.log('discovered Temperature and Humidity service');
      batteryService.discoverCharacteristics(['6e400003b5a3f393e0a9e50e24dcca9e'], function(error, characteristics) {
      //batteryService.discoverCharacteristics(['2a19'], function(error, characteristics) {
        var batteryLevelCharacteristic = characteristics[0];
        console.log('discovered sensor value characteristic');

        batteryLevelCharacteristic.on('data', function(data, isNotification) {
	 console.log(data.toString('utf8'));
        });

        // to enable notify
        batteryLevelCharacteristic.subscribe(function(error) {
          console.log('sensor value notification on');
        });
      });
    });
  });
 peripheral.once('disconnect', function() {
          console.log('Peripheral has been disconnected');
	  process.exit(0);
         });
  }
});
