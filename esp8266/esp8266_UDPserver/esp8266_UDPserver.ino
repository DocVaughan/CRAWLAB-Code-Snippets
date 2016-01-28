
/* ----------------------------------------------------------------------------

esp8266_UDPserver.ino

Basic UDP echo server

From: http://www.esp8266.com/viewtopic.php?f=29&t=2222

Created: 01/27/16
   - Joshua Vaughan
   - joshua.vaughan@louisiana.edu
   - http://www.ucs.louisiana.edu/~jev9637

 Modified:
   *

---------------------------------------------------------------------------- */

#include <stdio.h>

#include <ESP8266WiFi.h>
#include <WiFiUDP.h>

void printWifiStatus();

int status = WL_IDLE_STATUS;
const char* ssid = "Doc_Vaughan";  //  your network SSID (name)
const char* pass = "rougeourobots";       // your network password

unsigned int localPort = 2390;      // local port to listen for UDP packets

byte packetBuffer[512]; //buffer to hold incoming and outgoing packets

// A UDP instance to let us send and receive packets over UDP
WiFiUDP UDP;

char FriendlyReply[] = "Hello!";       // a string to send back

void setup()
{
  // Open serial communications and wait for port to open:
  Serial.begin(115200);
  while (!Serial) {
    ; // wait for serial port to connect. Needed for Leonardo only
  }

  // setting up Station AP
  WiFi.begin(ssid, pass);
  
  // Wait for connect to AP
  Serial.print("Connecting to ");
  Serial.print(ssid);
  
  int tries=0;
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
    tries++;
    if (tries > 30){
      break;
    }
  }
  Serial.println();


  printWifiStatus();

  Serial.println("Connected to WiFi");
  Serial.print("UDP server started at port ");
  Serial.println(localPort);
  UDP.begin(localPort);
}

void loop()
{
  int numBytes = UDP.parsePacket();
  
  if ( numBytes ) {
    Serial.print(millis() / 1000);
    Serial.print(":Packet of ");
    Serial.print(numBytes);
    Serial.print(" bytes received from ");
    Serial.print(UDP.remoteIP());
    Serial.print(":");
    Serial.println(UDP.remotePort());
    
    // We've received a packet, read the data from it
    int len = UDP.read(packetBuffer, numBytes); // read the packet into the buffer
    if (len > 0) packetBuffer[len-1] = 0;
    Serial.print(packetBuffer);

    // display the packet contents in HEX
    for (int i=1; i<=numBytes; i++){
      Serial.print(packetBuffer[i-1]);
      
      if (i % 32 == 0){
        Serial.println();
      }
      
      else Serial.print(' ');
    } // end for

    // send a reply to the IP address and port that sent us the packet we received
    UDP.beginPacket(UDP.remoteIP(), 2390);//UDP.remotePort());
    UDP.write(FriendlyReply);
    UDP.endPacket();
    
  } // end if
}

void printWifiStatus() {
  // print the SSID of the network you're attached to:
  Serial.print("SSID: ");
  Serial.println(WiFi.SSID());

  // print your WiFi shield's IP address:
  IPAddress ip = WiFi.localIP();
  Serial.print("IP Address: ");
  Serial.println(ip);
}
