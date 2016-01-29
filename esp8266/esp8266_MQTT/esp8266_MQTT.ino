/* ----------------------------------------------------------------------------
esp8266_MQTT.ino

Example use of the esp8266 for MQTT

The pubsubclient library (http://pubsubclient.knolleary.net) is needed to run

Based on example code from: http://pubsubclient.knolleary.net
Original "header" below

    Basic ESP8266 MQTT example
    
    This sketch demonstrates the capabilities of the pubsub library in combination
    with the ESP8266 board/library.
    
    It connects to an MQTT server then:
    - publishes "hello world" to the topic "outTopic" every two seconds
    - subscribes to the topic "inTopic", printing out any messages
    it receives. NB - it assumes the received payloads are strings not binary
    - If the first character of the topic "inTopic" is an 1, switch ON the ESP Led,
    else switch it off
    
    It will reconnect to the server if the connection is lost using a blocking
    reconnect function. See the 'mqtt_reconnect_nonblocking' example for how to
    achieve the same result without blocking the main loop.
    
    To install the ESP8266 board, (using Arduino 1.6.4+):
    - Add the following 3rd party board manager under 
      "File -> Preferences -> Additional Boards Manager URLs":
    http://arduino.esp8266.com/stable/package_esp8266com_index.json
    - Open the "Tools -> Board -> Board Manager" and click install for the ESP8266"
    - Select your ESP8266 in "Tools -> Board"

Created: 01/28/16
   - Joshua Vaughan
   - joshua.vaughan@louisiana.edu
   - http://www.ucs.louisiana.edu/~jev9637

 Modified:
   *

----------------------------------------------------------------------------*/


#include <ESP8266WiFi.h>
#include <PubSubClient.h>

// Update these with values suitable for your network.
const char* WIFI_SSID = "Doc_Vaughan";
const char* WIFI_PASSWORD = "rougeourobots";
const char* MQTT_SERVER = "iot.eclipse.org";
const int MQTT_PORT = 1883;

WiFiClient espClient;
PubSubClient client(espClient);
long lastMsg = 0;
char msg[50];
int value = 0;


void setup_wifi() {
  // This function setups up the Wi-Fi connection of the esp8266
  // It uses the constants defined above
  delay(10);
  
  // We start by connecting to a WiFi network
  Serial.println();
  Serial.print("Connecting to ");
  Serial.println(WIFI_SSID);

  WiFi.begin(WIFI_SSID, WIFI_PASSWORD);

  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }

  Serial.println("");
  Serial.println("Wi-Fi connected");
  Serial.println("IP address: ");
  Serial.println(WiFi.localIP());
}


void callback(char* topic, byte* payload, unsigned int length) {
  Serial.print("Message arrived:");
  Serial.print("\n\t Topic: ");
  Serial.print(topic);
  Serial.print("\t Data: ");
  
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
    if (client.connect("ESP8266Client")) {
      Serial.println(" connected");
      
      // Once connected, publish an announcement...
      client.publish("CRAWLAB/from_esp8266", "ESP8266 Connected!");
      // ... and resubscribe
      client.subscribe("CRAWLAB/#");
    } else {
      Serial.print(" failed with code rc = ");
      Serial.print(client.state());
      Serial.println(" Will try again in 5 seconds");
      
      // Wait 5 seconds before retrying
      delay(5000);
    }
  }
}


void setup() {
  // The initial setup function for the code
  // Sets up:
  //   * Serial communication
  //   * The Wi-Fi connection
  //   * The connection to the MQTT server    
  
  // Set up serial communication at 115200baud
  Serial.begin(115200);

  // Initialize the Wi-Fi network
  setup_wifi();
  
  // Set up the MQTT server
  client.setServer(MQTT_SERVER, MQTT_PORT);
  client.setCallback(callback);
}


void loop() {
  // The main() function 

  // If we're not connected try to connect
  if (!client.connected()) {
    reconnect();
  }
  client.loop();

  long now = millis();

  // Send "Hello World" every 2s
  if (now - lastMsg > 2000) {
    lastMsg = now;
    ++value;
    snprintf (msg, 75, "Hello World #%ld", value);

    Serial.println("");
    Serial.print("Publishing message: ");
    Serial.println(msg);
    Serial.println("");
    client.publish("CRAWLAB/from_esp8266", msg);
  }
}
