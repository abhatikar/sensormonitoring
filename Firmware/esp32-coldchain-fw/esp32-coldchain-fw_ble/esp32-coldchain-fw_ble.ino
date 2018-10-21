#include <BLEDevice.h>
#include <BLEServer.h>
#include <BLEUtils.h>
#include <BLE2902.h>
#include <Wire.h>
#include <Adafruit_Sensor.h>
#include "Adafruit_BME680.h"

Adafruit_BME680 bme; // I2C
const char* deviceID = "SeeCat03";

BLECharacteristic *pCharacteristic;

bool deviceConnected = false;

#define SERVICE_UUID            "6E400001-B5A3-F393-E0A9-E50E24DCCA9E" // UART service UUID
#define TMPDATA_CHAR_UUID       "6E400003-B5A3-F393-E0A9-E50E24DCCA9E"

class MyServerCallbacks: public BLEServerCallbacks {
    void onConnect(BLEServer* pServer) {
      deviceConnected = true;
    };

    void onDisconnect(BLEServer* pServer) {
      deviceConnected = false;
    };
};

void setup() {
    Serial.begin(115200);
    
    if (!bme.begin()) {
      Serial.println("Could not find a valid BME680 sensor, check wiring!");
      while (1);
    }
    // Set up oversampling and filter initialization
    bme.setTemperatureOversampling(BME680_OS_8X);
    bme.setHumidityOversampling(BME680_OS_2X);
    
    // Create the BLE Device
    BLEDevice::init(deviceID); // Give it a name
    
    // Create the BLE Server
    BLEServer *pServer = BLEDevice::createServer();
    pServer->setCallbacks(new MyServerCallbacks());
    
    // Create the BLE Service
    BLEService *pService = pServer->createService(SERVICE_UUID);
    
    // Create a BLE Characteristic
    pCharacteristic = pService->createCharacteristic(
                        TMPDATA_CHAR_UUID,
                        BLECharacteristic::PROPERTY_NOTIFY
                      );
    
    pCharacteristic->addDescriptor(new BLE2902());
    
    //Start the service
    pService->start();
    
    // Advertise the service
    pServer->getAdvertising()->start();
    Serial.println("Waiting a client connection to notify...");
}

void loop() {
  if (deviceConnected) {
    char msg[100];

  	if (! bme.performReading()) {
      		Serial.println("Failed to perform reading :(");
      		return;
    }
  	Serial.print("Temperature = ");
  	Serial.print(bme.temperature);
  	Serial.println(" *C");
  
  	Serial.print("Humidity = ");
  	Serial.print(bme.humidity);
  	Serial.println(" %");
  
    snprintf (msg, 100, "{\"temperature\" : \"%2.2f\", \"humidity\" : \"%2.2f\", \"deviceId\" : \"%s\" }", bme.temperature, bme.humidity, deviceID);
        
    pCharacteristic->setValue(msg);
    pCharacteristic->notify();
    Serial.print("*** Data sent: ");
    Serial.print(msg);
    Serial.println(" ***");
    delay(5000);
  }
}
