/* ----------------------------------------------------------------------------
esp8266_WemoD1_MQTT.ino

Code to receive control and parse control packets for the cable-driven
system's motor boxes. Data is passed from MQTT to the SH2 over serial

This script is set up for the Wemo D1 mini board

LED blinks according to status of the communications:
  * Blinks every 250ms when trying to connect to WiFi
  * Blinks every 5s when trying to connect to MQTT

The pubsubclient library (http://pubsubclient.knolleary.net) is needed to run

Derived from example code at: http://pubsubclient.knolleary.net


Created: 05/30/16
   - Joshua Vaughan
   - joshua.vaughan@louisiana.edu
   - http://www.ucs.louisiana.edu/~jev9637

----------------------------------------------------------------------------*/

#include <ESP8266WiFi.h>
#include <PubSubClient.h>

// Function prototypes as necessary
int readline(int readch, char *buffer, int len);

// Update these to match desired WiFi and MQTT broker
//const char* WIFI_SSID = "Doc_Vaughan";
//const char* WIFI_PASSWORD = "rougeourobots";
const char* WIFI_SSID = "West Ettrick";
const char* WIFI_PASSWORD = "LeroyMoney";
const char* MQTT_SERVER = "iot.eclipse.org";
const int MQTT_PORT = 1883;

WiFiClient espClient;
PubSubClient client(espClient);

// MQTT and serial strings
char msg[50];           // Holds messages to send over MQTT
char data_string[50];   // Parsed data received over MQTT
char serial_string[16]; // string holding incoming serial data

// housekeeping variables
long lastMsg = 0;
int value = 0;

// Define LED pin number
const byte LED = 2;

// constants to store box specific info (change for each box)
const byte BOX_NUMBER = 1;
const char* BOX_ID_STRING = "CRAWLAB_Cable_Box1";
const char* BOX_PUB_TOPIC = "CRAWLAB/from_cable1";

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


void MQTT_callback(char* topic, byte* payload, unsigned int length) {
  if (DEBUGGING) {
    Serial.print("Message arrived:");
    Serial.print("\n\t Topic: ");
    Serial.print(topic);
    Serial.print("\t Data: ");

    // Toggle the LED on each piece of data received
    digitalWrite(LED, !digitalRead(LED));
  }

  // loop over string received to create data_string to send to SH2
  for (int i = 0; i < length; i++) {
    sprintf(data_string, "%s%c", data_string, (char)payload[i]);
  }
  Serial.println(data_string);
  
  // Empty data_string after sending via serial
  sprintf(data_string,"");
}


void reconnect_MQTT() {
  // Loop until we're reconnected
  while (!client.connected()) {
    if (DEBUGGING) {
      Serial.print("Attempting MQTT connection...");
    }
    
    // Attempt to connect
    if (client.connect(BOX_ID_STRING)) {
      if (DEBUGGING) {
          Serial.println(" connected");
      }

      // Blink the LED rapidly once connected to MQTT
      for (int counter = 0; counter <= 10; counter++) {
          digitalWrite(LED, HIGH);
          delay(100);
          digitalWrite(LED, LOW);
          delay(100);
      }
      
      // Once connected, publish an announcement...
      sprintf(msg, "Cable Motor Box %d ESP8266 Connected!", BOX_NUMBER);
      client.publish(BOX_PUB_TOPIC, msg);
      // ... and resubscribe
      client.subscribe("CRAWLAB/to_cable");
    } 
    else {
      if (DEBUGGING) {
          Serial.print(" failed with code rc = ");
          Serial.print(client.state());
          Serial.println(" Will try again in 5 seconds");
      }
      
      // Wait 5 seconds before retrying, leave LED lit during the wait
      digitalWrite(LED, HIGH);
      delay(5000);
      digitalWrite(LED, LOW);
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

  // Set up LED pin as output, used as indicator of WiFi Connection
  pinMode(LED, OUTPUT);
  
  // Initialize the Wi-Fi network
  setup_wifi();
  
  // Set up the MQTT server
  client.setServer(MQTT_SERVER, MQTT_PORT);
  client.setCallback(MQTT_callback);
}


void loop() {
  
  // If we're not connected try to connect
  if (!client.connected()) {
    reconnect_MQTT();
  }

  client.loop();

  // Get the Serial Data from the SH2
  if (readline(Serial.read(), serial_string, 16) > 0) {

    digitalWrite(LED, !digitalRead(LED));
    
    if (DEBUGGING) {
      Serial.print("Received from SH2: ");
      Serial.println(serial_string);   
    }
    
    client.publish(BOX_PUB_TOPIC, serial_string);
  }
}

int readline(int readch, char *buffer, int len) {
  // Adapted from: https://hackingmajenkoblog.wordpress.com/2016/02/01/reading-serial-on-the-arduino/
  static int pos = 0;
  int rpos;

  if (readch > 0) {
    switch (readch) {
      case '\r': // Return on CR
//        break;
      case 0x0A: //'\r': wait for new-lines
        rpos = pos;
        pos = 0;  // Reset position index ready for next time
        return rpos;
      default:
        if (pos < len-1) {
          buffer[pos++] = readch;
          buffer[pos] = 0;
        }
    }
  }
  // No end of line has been found, so return -1.
  return -1;
}
