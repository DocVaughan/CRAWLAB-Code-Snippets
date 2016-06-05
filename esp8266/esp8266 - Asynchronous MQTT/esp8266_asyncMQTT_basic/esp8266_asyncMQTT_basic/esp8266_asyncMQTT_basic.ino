
/* ----------------------------------------------------------------------------

esp8266_asyncMQTT_basic.ino

Basic implementation of asynchronous MQTT operations

Adapted from:
  - https://github.com/marvinroger/async-mqtt-client

Necessary libraries:
  - async-mqtt-client - https://github.com/marvinroger/async-mqtt-client
  - ESPAsyncTCP - https://github.com/me-no-dev/ESPAsyncTCP

Created: 06/05/16
   - Joshua Vaughan
   - joshua.vaughan@louisiana.edu
   - http://www.ucs.louisiana.edu/~jev9637

 Modified:
   *

---------------------------------------------------------------------------- */

#include <stdio.h>

#include <ESP8266WiFi.h>
#include <AsyncMqttClient.h>

AsyncMqttClient mqttClient;

// Update these to match desired WiFi network
const char* WIFI_SSID = "Doc_Vaughan";
const char* WIFI_PASSWORD = "rougeourobots";

// Update these to match desired MQTT broker
const char* MQTT_SERVER = "iot.eclipse.org";
const int MQTT_PORT = 1883;
const char* MQTT_USERNAME = "user_name";
const char* MQTT_PASSWORD = "password";
const char* MQTT_CLIENT_ID = "CRAWLABesp8266";

// Define LED pin number
const byte LED = 0;

// set true to print debug statements to serial out
const bool DEBUGGING = false; 


void setup_wifi() {
  // This function setups up the Wi-Fi connection of the esp8266
  // It uses the constants defined above
  delay(10);
  
  // We start by connecting to a WiFi network
  if (DEBUGGING) {  
    Serial.println();
    Serial.print("Connecting to ");
    Serial.println(WIFI_SSID);
  }

  WiFi.begin(WIFI_SSID, WIFI_PASSWORD);

  // Blink an LED while trying to connect
  while (WiFi.status() != WL_CONNECTED) {
    digitalWrite(LED, HIGH);
    delay(250);
    digitalWrite(LED, LOW);
    delay(250);
  }
  
  if (DEBUGGING) {
    Serial.println("");
    Serial.println("Wi-Fi connected");
    Serial.println("IP address: ");
    Serial.println(WiFi.localIP());
  }
}


void onMqttConnect() {
  Serial.println("Connected to the broker");
  
  uint16_t packetIdSub = mqttClient.subscribe("CRAWLAB/#", 2);
  Serial.print("Subscribing at QoS 2, packetId: ");
  Serial.println(packetIdSub);
  
  mqttClient.publish("CRAWLAB/connectionTest", 0, true, "test 1");
  Serial.println("Publishing at QoS 0");
  
  uint16_t packetIdPub1 = mqttClient.publish("CRAWLAB/connectionTest", 1, true, "test 2");
  Serial.print("Publishing at QoS 1, packetId: ");
  Serial.println(packetIdPub1);
  
  uint16_t packetIdPub2 = mqttClient.publish("CRAWLAB/connectionTest", 2, true, "test 3");
  Serial.print("Publishing at QoS 2, packetId: ");
  Serial.println(packetIdPub2);
}


void onMqttDisconnect(AsyncMqttClientDisconnectReason reason) {
  Serial.println("Disconnected from the broker.");
  Serial.println("Reconnecting to MQTT...\n");
  mqttClient.connect();
}


void onMqttSubscribe(uint16_t packetId, uint8_t qos) {
  Serial.println("Subscribe acknowledged");
  Serial.print("  packetId: ");
  Serial.println(packetId);
  Serial.print("  QoS: ");
  Serial.println(qos);
}


void onMqttUnsubscribe(uint16_t packetId) {
  Serial.println("Unsubscribe acknowledged");
  Serial.print("  packetId: ");
  Serial.println(packetId);
}


void onMqttMessage(const char* topic, const char* payload, uint8_t qos, size_t len, size_t index, size_t total) {
  Serial.println("\nMessage received");
  Serial.print("  Topic:   \t");
  Serial.println(topic);
  Serial.print("  QoS:     \t");
  Serial.println(qos);
  Serial.print("  Len:     \t");
  Serial.println(len);
  Serial.print("  Index:   \t");
  Serial.println(index);
  Serial.print("  Total:   \t");
  Serial.println(total);
  Serial.print("  Payload: \t");
  Serial.println(payload);
}


void onMqttPublish(uint16_t packetId) {
  Serial.println("Publish acknowledged");
  Serial.print("  packetId: ");
  Serial.println(packetId);
}


void setup() {
  // Set up serial communication at 115200baud
  Serial.begin(115200);

  // Set up LED pin as output, used as indicator of WiFi Connection
  pinMode(LED, OUTPUT);
  
  // Initialize the Wi-Fi network
  setup_wifi();

  // Now define all the MQTT callback functions
  mqttClient.onConnect(onMqttConnect);
  mqttClient.onDisconnect(onMqttDisconnect);
  mqttClient.onSubscribe(onMqttSubscribe);
  mqttClient.onUnsubscribe(onMqttUnsubscribe);
  mqttClient.onMessage(onMqttMessage);
  mqttClient.onPublish(onMqttPublish);
  mqttClient.setServer(MQTT_SERVER, MQTT_PORT);
  //mqttClient.setKeepAlive(5).setWill("CRAWLAB/online", 2, true, "offline").setCredentials(MQTT_USERNAME, MQTT_PASSWORD).setClientId("CRAWLABesp8266");
  mqttClient.setKeepAlive(5).setWill("CRAWLAB/online", 2, true, "offline").setClientId(MQTT_CLIENT_ID);
  
  // Connect to the MQTT broker
  Serial.println("Connecting to MQTT Broker...");
  mqttClient.connect();
}


void loop() {
  // publish hello every 5s
  mqttClient.publish("CRAWLAB/", 2, false, "Hello from esp8266");

  // Because this library is asynchronous, we will still be able to receive data even during the delay function
  // during which the process would normally be completely "sleeping"
  delay(5000);
  
}
