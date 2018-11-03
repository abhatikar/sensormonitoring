
#include <BLEDevice.h>
#include <BLEUtils.h>
#include <BLEServer.h>
#include <esp_deep_sleep.h>
#include <Adafruit_Sensor.h>
#include "Adafruit_BME680.h"


Adafruit_BME680 bme; // I2C
const char* deviceID = "SeeCat04";

BLEAdvertisementData advert;
BLEAdvertising *pAdvertising;

//manufacturer code (0x02E5 for Espressif)
int man_code = 0x02E5;

//function takes String and adds manufacturer code at the beginning
void setManData(String c, BLEAdvertisementData &adv, int m_code) {

  String s;
  char b2 = (char)(m_code >> 8);
  m_code <<= 8;
  char b1 = (char)(m_code >> 8);
  s.concat(b1);
  s.concat(b2);
  s.concat(c);

  adv.setManufacturerData(s.c_str());
}

#define uS_TO_S_FACTOR 1000000  /* Conversion factor for micro seconds to seconds */
#define TIME_TO_SLEEP  5        /* Time ESP32 will go to sleep (in seconds) */

RTC_DATA_ATTR int bootCount = 0;

/*
Method to print the reason by which ESP32
has been awaken from sleep
*/
void print_wakeup_reason(){
  esp_deep_sleep_wakeup_cause_t wakeup_reason;

  wakeup_reason = esp_deep_sleep_get_wakeup_cause();

  switch(wakeup_reason)
  {
    case 1  : Serial.println("Wakeup caused by external signal using RTC_IO"); break;
    case 2  : Serial.println("Wakeup caused by external signal using RTC_CNTL"); break;
    case 3  : Serial.println("Wakeup caused by timer"); break;
    case 4  : Serial.println("Wakeup caused by touchpad"); break;
    case 5  : Serial.println("Wakeup caused by ULP program"); break;
    default : Serial.println("Wakeup was not caused by deep sleep"); break;
  }
}

void setup() {
  Serial.begin(115200);

  delay(1000); //Take some time to open up the Serial Monitor

  //Increment boot number and print it every reboot
  ++bootCount;
  Serial.println("Boot number: " + String(bootCount));

  //Print the wakeup reason for ESP32
  print_wakeup_reason();

  /*
  First we configure the wake up source
  We set our ESP32 to wake up every 5 seconds
  */
  esp_deep_sleep_enable_timer_wakeup(TIME_TO_SLEEP * uS_TO_S_FACTOR);
  Serial.println("Setup ESP32 to sleep for every " + String(TIME_TO_SLEEP) +
  " Seconds");

  char msg[12] = {0};

  if (!bme.begin()) {
    Serial.println("Could not find a valid BME680 sensor, check wiring!");
    while (1);
  }
  // Set up oversampling and filter initialization
  bme.setTemperatureOversampling(BME680_OS_8X);
  bme.setHumidityOversampling(BME680_OS_2X);

  Serial.println("Starting BLE work!");

  BLEDevice::init(deviceID);
  BLEServer *pServer = BLEDevice::createServer();

  pAdvertising = pServer->getAdvertising();
  advert.setName(deviceID);
  pAdvertising->setAdvertisementData(advert);
  //pAdvertising->start();

   if (! bme.performReading()) {
        Serial.println("Failed to perform reading :(");
        return;
  }

  snprintf (msg, 12, "%2.2f,%2.2f", bme.temperature, bme.humidity);
  Serial.println(msg);

  BLEAdvertisementData scan_response;

  setManData(msg, scan_response, man_code);

  //pAdvertising->stop();
  pAdvertising->setScanResponseData(scan_response);
  pAdvertising->start();

  delay(5000);

  Serial.println("Going to sleep now");
  esp_deep_sleep_start();
  Serial.println("This will never be printed");
}

void loop() {

}
