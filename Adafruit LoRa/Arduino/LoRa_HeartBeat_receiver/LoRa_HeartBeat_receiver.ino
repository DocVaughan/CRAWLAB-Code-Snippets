/* ----------------------------------------------------------------------------

LoRa_HeartBeat_receiver.ino

Arduino sketch to receive heartbeat messages and change the color of the onboard 
LED based on current status. 

Intended for use with the Feather M0 with LoRa Radio:
  * https://www.adafruit.com/product/3178

Modified from the example code at Adafruit's Tutorial:
  * https://learn.adafruit.com/adafruit-feather-m0-radio-with-lora-radio-module/using-the-rfm-9x-radio

Created: 05/09/19
   - Joshua Vaughan
   - joshua.vaughan@louisiana.edu
   - http://www.ucs.louisiana.edu/~jev9637

 Modified:
   *

---------------------------------------------------------------------------- */

#include <SPI.h>
#include <RH_RF95.h>

/* for Feather32u4 RFM9x
#define RFM95_CS 8
#define RFM95_RST 4
#define RFM95_INT 7
*/

// for feather m0 RFM9x
#define RFM95_CS 8
#define RFM95_RST 4
#define RFM95_INT 3


/* for shield 
#define RFM95_CS 10
#define RFM95_RST 9
#define RFM95_INT 7
*/

/* Feather 32u4 w/wing
#define RFM95_RST     11   // "A"
#define RFM95_CS      10   // "B"
#define RFM95_INT     2    // "SDA" (only SDA/SCL/RX/TX have IRQ!)
*/

/* Feather m0 w/wing 
#define RFM95_RST     11   // "A"
#define RFM95_CS      10   // "B"
#define RFM95_INT     6    // "D"
*/

#if defined(ESP8266)
  /* for ESP w/featherwing */ 
  #define RFM95_CS  2    // "E"
  #define RFM95_RST 16   // "D"
  #define RFM95_INT 15   // "B"

#elif defined(ESP32)  
  /* ESP32 feather w/wing */
  #define RFM95_RST     27   // "A"
  #define RFM95_CS      33   // "B"
  #define RFM95_INT     12   //  next to A

#elif defined(NRF52)  
  /* nRF52832 feather w/wing */
  #define RFM95_RST     7   // "A"
  #define RFM95_CS      11   // "B"
  #define RFM95_INT     31   // "C"
  
#elif defined(TEENSYDUINO)
  /* Teensy 3.x w/wing */
  #define RFM95_RST     9   // "A"
  #define RFM95_CS      10   // "B"
  #define RFM95_INT     4    // "C"
#endif


// Change to 434.0 or other frequency, must match RX's freq!
#define RF95_FREQ 915.0

// Singleton instance of the radio driver
RH_RF95 rf95(RFM95_CS, RFM95_INT);

// Blinky on receipt
#define LED 13

void setup()
{
  pinMode(LED, OUTPUT);
  pinMode(RFM95_RST, OUTPUT);
  digitalWrite(RFM95_RST, HIGH);

  Serial.begin(115200);
  while (!Serial) {
    delay(1);
  }
  delay(100);

  // manual reset
  digitalWrite(RFM95_RST, LOW);
  delay(10);
  digitalWrite(RFM95_RST, HIGH);
  delay(10);

  while (!rf95.init()) {
    Serial.println("LoRa radio init failed");
    while (1);
  }
  Serial.println("LoRa radio init OK!");

  // Defaults after init are 434.0MHz, modulation GFSK_Rb250Fd250, +13dbM
  if (!rf95.setFrequency(RF95_FREQ)) {
    Serial.println("setFrequency failed");
    while (1);
  }
  Serial.print("Set Freq to: "); Serial.println(RF95_FREQ);

  // Defaults after init are 434.0MHz, 13dBm, Bw = 125 kHz, Cr = 4/5, Sf = 128chips/symbol, CRC on

  // The default transmitter power is 13dBm, using PA_BOOST.
  // If you are using RFM95/96/97/98 modules which uses the PA_BOOST transmitter pin, then
  // you can set transmitter powers from 5 to 23 dBm:
  rf95.setTxPower(23, false);
}

void loop() {
    const char HEARTBEAT_MESSAGE[] = "$ULheartbeat";
    const int HEARTBEAT_MESSAGE_LENGTH = sizeof(HEARTBEAT_MESSAGE) - 1;
    static int num_missed_heartbeats = 0;
    const int MAX_MISSED_HEARTBEATS = 5;
    
    if (rf95.available()) {
        // Should be a message for us now
        uint8_t buf[RH_RF95_MAX_MESSAGE_LEN];
        uint8_t len = sizeof(buf);
    
        if (rf95.recv(buf, &len)) {
            // Here, we'll always indicate that we received a message
            // In operation, we probably don't want to always print this out
            digitalWrite(LED, HIGH);
            RH_RF95::printBuffer("Received: ", buf, len);
            Serial.print("Got: ");
            Serial.println((char*)buf);
            
            // This will print the signal strength of the last message received.
            // TODO: 05/09/19 - JEV - We probably want to move this to apply only
            //                        to messages we have identified as properly-
            //                        formatted heartbeats
            Serial.print("RSSI: ");
            Serial.println(rf95.lastRssi(), DEC);

            // Compare the message received with the HEARTBEAT_MESSAGE expected
            // If it doesn't match, increment the num_missed_heartbeats counter
            // If it does, reset the counter and send an acknowledgement message
            if (strncmp((char*)buf, HEARTBEAT_MESSAGE, HEARTBEAT_MESSAGE_LENGTH) != 0) {
              Serial.println("Heartbeat missed");
              num_missed_heartbeats = num_missed_heartbeats + 1;
            }
            else {
                // reset missed heartbeat counter 
                num_missed_heartbeats = 0;
                
                // Send a reply
                uint8_t data[] = "$UL_ACK";
                rf95.send(data, sizeof(data));
                rf95.waitPacketSent();
                Serial.println("Sent a reply");
                digitalWrite(LED, LOW);
            }
        }
    }
    else { 
        // If there was no data availalbe, we also increment the num_missed_heartbeats counter
        num_missed_heartbeats = num_missed_heartbeats + 1;
    }

    // Now, check if we've exceeded the maximum number of missed beats
    if (num_missed_heartbeats < MAX_MISSED_HEARTBEATS) {
        Serial.println("Heartbeat missed");
    }
    else if (num_missed_heartbeats == MAX_MISSED_HEARTBEATS) {
        Serial.println("Heartbeat missed");
        Serial.println("Missed too many heartbeats!!!");
        digitalWrite(LED, HIGH);
    }
    else {
        digitalWrite(LED, HIGH);
    }

    delay(100); // sleep 100ms
}
