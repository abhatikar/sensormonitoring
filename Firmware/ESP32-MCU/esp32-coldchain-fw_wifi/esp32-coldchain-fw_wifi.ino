#include <WiFi.h>
#include <PubSubClient.h>
#include <Wire.h>
#include <Adafruit_Sensor.h>
#include "Adafruit_BME680.h"
#include <ESPmDNS.h>
#include <ArduinoOTA.h>
#include <NTPClient.h>
#include <WiFiUdp.h>

//#define MYWATCHDOG 1

Adafruit_BME680 bme; // I2C

#ifdef MYWATCHDOG
WiFiUDP ntpUDP;
//NTPClient timeClient(ntpUDP);
NTPClient timeClient(ntpUDP, "europe.pool.ntp.org", 3600, 60000);
#endif

//const char* ssid = "AP_ID";
//const char* password =  "passwd";
const char* mqtt_server = "iot.eclipse.org";

const char* deviceID = "SeeCat02";
const char* sensorDataTopic = "deviceID/SeeCat02/sensorData";

WiFiClient espClient;
PubSubClient client(espClient);
long lastMsg = 0;
int value = 0;
  
void connectToNetwork() {
  WiFi.begin();
  delay(5000);

  if (WiFi.status() != WL_CONNECTED) {
    /* Set ESP32 to WiFi Station mode */
    WiFi.mode(WIFI_AP_STA);
    /* start SmartConfig */
    WiFi.beginSmartConfig();
  
    /* Wait for SmartConfig packet from mobile */
    Serial.println("Waiting for SmartConfig.");
    while (!WiFi.smartConfigDone()) {
      //digitalWrite(LED_BUILTIN, HIGH);
      delay(500);
      Serial.print(".");
      //digitalWrite(LED_BUILTIN, LOW);
    }
    Serial.println("");
    Serial.println("SmartConfig done.");
    /* Wait for WiFi to connect to AP */
    Serial.println("Waiting for WiFi");
    while (WiFi.status() != WL_CONNECTED) {
      delay(500);
      Serial.print(".");
    }
    Serial.println("WiFi Connected.");
    Serial.print("IP Address: ");
    Serial.println(WiFi.localIP());
    Serial.println("Connected to network");        
  }
  // Set up mDNS responder:
  // - first argument is the domain name, in this example
  //   the fully-qualified domain name is "esp8266.local"
  // - second argument is the IP address to advertise
  //   we send our IP address on the WiFi network
  if (!MDNS.begin(deviceID)) {
      Serial.println("Error setting up MDNS responder!");
      while(1) {
          delay(1000);
      }
  }
  Serial.println("mDNS responder started");
}
 
void setup() {
  Serial.begin(115200);
  while (!Serial);
    connectToNetwork();
  Serial.println(WiFi.macAddress());
  Serial.println(WiFi.localIP());

#ifdef MYWATCHDOG
  timeClient.begin();
#endif
   
  ArduinoOTA.setHostname(deviceID);
  ArduinoOTA.setPassword("esp32");

  ArduinoOTA.onStart([]() {
    Serial.println("Start");
  });
  ArduinoOTA.onEnd([]() {
    Serial.println("\nEnd");
  });
  ArduinoOTA.onProgress([](unsigned int progress, unsigned int total) {
    Serial.printf("Progress: %u%%\r", (progress / (total / 100)));
  });
  ArduinoOTA.onError([](ota_error_t error) {
    Serial.printf("Error[%u]: ", error);
    if (error == OTA_AUTH_ERROR) Serial.println("Auth Failed");
    else if (error == OTA_BEGIN_ERROR) Serial.println("Begin Failed");
    else if (error == OTA_CONNECT_ERROR) Serial.println("Connect Failed");
    else if (error == OTA_RECEIVE_ERROR) Serial.println("Receive Failed");
    else if (error == OTA_END_ERROR) Serial.println("End Failed");
  });
  ArduinoOTA.begin();
  Serial.println("OTA ready");

  client.setServer(mqtt_server, 1883);
  client.setCallback(callback);

  if (!bme.begin()) {
    Serial.println("Could not find a valid BME680 sensor, check wiring!");
    while (1);
  }
  // Set up oversampling and filter initialization
  bme.setTemperatureOversampling(BME680_OS_8X);
  bme.setHumidityOversampling(BME680_OS_2X);
}

void callback(char* topic, byte* payload, unsigned int length) {
  Serial.print("Message arrived [");
  Serial.print(topic);
  Serial.print("] ");
  for (int i = 0; i < length; i++) {
    Serial.print((char)payload[i]);
  }
  Serial.println();
}

void reconnect() {
  // Loop until we're reconnected
  while (!client.connected()) {
    Serial.print("Attempting MQTT connection...");
    // Attempt to connect
    if (client.connect(deviceID)) {
      Serial.println("connected");
      // Once connected, publish an announcement...
      //client.publish("outTopic", "hello world");
      // ... and resubscribe
      //client.subscribe("inTopic");
    } else {
      Serial.print("failed, rc=");
      Serial.print(client.state());
      Serial.println(" try again in 5 seconds");
      // Wait 5 seconds before retrying
      delay(5000);
    }
  }
}

void loop() {

#ifdef MYWATCHDOG 
  timeClient.update();
  Serial.println(timeClient.getFormattedTime());
#endif

  ArduinoOTA.handle();
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

  if (!client.connected()) {
    reconnect();
  }
  client.loop();

  long now = millis();
  if (now - lastMsg > 5000) {
    char msg[100];
    lastMsg = now;
    ++value;
    snprintf (msg, 100, "{\"temperature\" : \"%2.2f\", \"humidity\" : \"%2.2f\", \"deviceId\" : \"%s\" }", bme.temperature, bme.humidity, deviceID);
    Serial.print("Publish Sensor Data: ");
    Serial.println(msg);
    client.publish(sensorDataTopic, msg);
  }

  Serial.println();
  delay(5000);
}
