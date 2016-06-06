
/* ----------------------------------------------------------------------------

esp8266_WebSocketClient_Basic.ino

Basic websocket client on the ESP8266

Required Library:
  - Arduino-Websocket-Fast - https://github.com/u0078867/Arduino-Websocket-Fast

Created: 06/05/16
   - Joshua Vaughan
   - joshua.vaughan@louisiana.edu
   - http://www.ucs.louisiana.edu/~jev9637

 Modified:
   *

---------------------------------------------------------------------------- */

#include <stdio.h>
#include <ESP8266WiFi.h>
#include <WebSocketClient.h>

// Here we define a maximum framelength to 64 bytes. Default is 256.
#define MAX_FRAME_LENGTH 64

// Define how many callback functions you have. Default is 1.
#define CALLBACK_FUNCTIONS 1

// Update these to match desired WiFi network
const char* WIFI_SSID = "Doc_Vaughan";
const char* WIFI_PASSWORD = "rougeourobots";


// Update these to match the desired websocket server
char* WEBSOCKET_HOST = "10.0.1.3"; //"echo.websocket.org"; 
char* WEBSOCKET_PATH = "/";
const int WEBSOCKET_TCPPORT = 8080;


// set true to print debug statements to serial out
const bool DEBUGGING = false; 

// Define LED pin number
const byte LED = 2;

// Declare TCP and websocket client objects
WiFiClient client;
WebSocketClient webSocketClient;

// Define the time that we exit setup and start running loop() (approximately)
float start_time;


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


void setup() {
  // The initial setup function for the code
  // Sets up:
  //   * Serial communication
  //   * The Wi-Fi connection
  //   * The websocket connection
  
  // Set up serial communication at 115200baud
  Serial.begin(115200);

  // Set up LED pin as output, used as indicator of WiFi Connection
  pinMode(LED, OUTPUT);
  
  // Initialize the Wi-Fi network
  setup_wifi();
  bool not_connected_to_websocket = true;
  
  while (not_connected_to_websocket) {
    // Connect to the websocket server
    Serial.println("Atttempting to connect to websocket server.");
    while (!client.connect(WEBSOCKET_HOST, WEBSOCKET_TCPPORT)) {
          Serial.println("Connection failed. Attempting again in 1 second.");
          delay(1000);
    } 
    Serial.println("Connected.");
  
    // Handshake with the server
    webSocketClient.path = WEBSOCKET_PATH;
    webSocketClient.host = WEBSOCKET_HOST;
    
    if (webSocketClient.handshake(client)) {
      Serial.println("Handshake successful");
      not_connected_to_websocket = true;
    }
    else {
      Serial.println("Handshake failed. Trying again in 1 second");
      delay(1000);
    }
  }

  // Define the time that we exit setup and start running loop() (approximately)
  start_time = millis();
}

void loop() {
  String data;
  float test_data = 0.0;
  String send_data;

  // Test data is just a 0.5Hz sin wave
  test_data = sin(3.14 * (millis() - start_time)) + 1;

  if (client.connected()) {

    // get the data
    webSocketClient.getData(data);

    // if we got data, print it out
    if (data.length() > 0) {
      Serial.print("Received data: ");
      Serial.println(data);
    }

    // Send some data back
    send_data = String(test_data);
    webSocketClient.sendData(send_data);

  } 
  else {
    Serial.println("Client disconnected.");
  }

  // wait 10ms between loops
  delay(10);
}
