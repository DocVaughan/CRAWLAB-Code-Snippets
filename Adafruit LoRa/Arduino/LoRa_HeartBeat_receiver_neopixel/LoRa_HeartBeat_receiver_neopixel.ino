/* ----------------------------------------------------------------------------

LoRa_HeartBeat_receiver_neopixel.ino

Arduino sketch to receive heartbeat messages and change the color of a NeoPixel 
strand based on current status. The strand also does a "Knight Rider" effect
since moving colors are easier to see than static ones.

Intended for use with the Feather M0 with LoRa Radio:
  * https://www.adafruit.com/product/3178

Modified from the example code at Adafruit's Tutorial:
  * https://learn.adafruit.com/adafruit-feather-m0-radio-with-lora-radio-module/using-the-rfm-9x-radio
  * https://learn.adafruit.com/adafruit-neopixel-uberguide/arduino-library-use

Created: 05/09/19
   - Joshua Vaughan
   - joshua.vaughan@louisiana.edu
   - http://www.ucs.louisiana.edu/~jev9637

 Modified:
   *

---------------------------------------------------------------------------- */

#include <stdio.h>
#include <SPI.h>
#include <RH_RF95.h>
#include <Adafruit_NeoPixel.h>

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
  #define RFM95_RST     7    // "A"
  #define RFM95_CS      11   // "B"
  #define RFM95_INT     31   // "C"
  
#elif defined(TEENSYDUINO)
  /* Teensy 3.x w/wing */
  #define RFM95_RST     9    // "A"
  #define RFM95_CS      10   // "B"
  #define RFM95_INT     4    // "C"
#endif


// Change to 434.0 or other frequency, must match RX's freq!
#define RF95_FREQ 915.0

// Singleton instance of the radio driver
RH_RF95 rf95(RFM95_CS, RFM95_INT);

// Onboard LED pin
#define LED 13

// Which pin on the Arduino is connected to the NeoPixels?
#define LED_PIN    6

// How many NeoPixels are attached to the Arduino?
#define LED_COUNT 30

// Declare our NeoPixel strip object:
Adafruit_NeoPixel strip(LED_COUNT, LED_PIN, NEO_GRB + NEO_KHZ800);
// Argument 1 = Number of pixels in NeoPixel strip
// Argument 2 = Arduino pin number (most are valid)
// Argument 3 = Pixel type flags, add together as needed:
//   NEO_KHZ800  800 KHz bitstream (most NeoPixel products w/WS2812 LEDs)
//   NEO_KHZ400  400 KHz (classic 'v1' (not v2) FLORA pixels, WS2811 drivers)
//   NEO_GRB     Pixels are wired for GRB bitstream (most NeoPixel products)
//   NEO_RGB     Pixels are wired for RGB bitstream (v1 FLORA pixels, not v2)
//   NEO_RGBW    Pixels are wired for RGBW bitstream (NeoPixel RGBW products)

// Define some colors for the NeoPixels
uint32_t RED_LOW = strip.Color(32, 0, 0);
uint32_t RED_MED = strip.Color(64, 0, 0);
uint32_t RED_HIGH = strip.Color(255, 0, 0);
uint32_t GREEN_LOW = strip.Color(0, 32, 0);
uint32_t GREEN_MED = strip.Color(0, 64, 0);
uint32_t GREEN_HIGH = strip.Color(0, 255, 0);
uint32_t BLUE_LOW = strip.Color(0, 0, 32);
uint32_t BLUE_MED = strip.Color(0, 0, 64);
uint32_t BLUE_HIGH = strip.Color(0, 0, 255);
uint32_t YELLOW_LOW = strip.Color(16, 32, 0);
uint32_t YELLOW_MED = strip.Color(32, 64, 0);
uint32_t YELLOW_HIGH = strip.Color(128, 255, 0);
uint32_t WHITE_LOW = strip.Color(32, 32, 32);
uint32_t WHITE_MED = strip.Color(64, 64, 64);
uint32_t WHITE_HIGH = strip.Color(255, 255, 255);


void setup() {
    pinMode(LED, OUTPUT);
    pinMode(RFM95_RST, OUTPUT);
    digitalWrite(RFM95_RST, HIGH);

    Serial.begin(115200);

    // Wait for the serial monitor to open
    // Be sure to comment this out in application
//    while (!Serial) {
//        delay(1);
//    }
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

    // Now, set up the NeoPixels
    strip.begin();            // INITIALIZE NeoPixel strip object (REQUIRED)
    strip.show();             // Turn OFF all pixels ASAP
    strip.setBrightness(128); // Set BRIGHTNESS to about 1/2 (max = 255)
}

void loop() {
    const char HEARTBEAT_MESSAGE[] = "$ULheartbeat";
    const int HEARTBEAT_MESSAGE_LENGTH = sizeof(HEARTBEAT_MESSAGE) - 1;
    static int num_missed_heartbeats = 0;
    const int MAX_MISSED_HEARTBEATS = 5;

    static uint8_t going = 1;
    static uint8_t pixel_index = 0;

    unsigned long start_time;
    unsigned long elapsed_time;
    start_time = millis();
    
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
              Serial.println("Heartbeat didn't match.");
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
        
        if (num_missed_heartbeats < MAX_MISSED_HEARTBEATS) {
            Serial.println("Heartbeat missed");    
        }
    }

    // Now, check if we've exceeded the maximum number of missed beats
    // and process the NeoPixel colors accordingly
    if (num_missed_heartbeats < MAX_MISSED_HEARTBEATS) {
        // Turn the neopixels green
        strip.fill(GREEN_MED, 0);

        if (pixel_index + 5 >= LED_COUNT) {
            going = 0;
        }
        else if (pixel_index <= 0) {
            going = 1;
        }

        if (going) {
            strip.fill(GREEN_HIGH, pixel_index, 5);              
            pixel_index = pixel_index + 1;
        }
        else {
            strip.fill(GREEN_HIGH, pixel_index, 5);
            pixel_index = pixel_index - 1;
        }
    }
    else if (num_missed_heartbeats == MAX_MISSED_HEARTBEATS) {
        Serial.println("Heartbeat missed");
        Serial.println("Missed too many heartbeats!!!");
        digitalWrite(LED, HIGH);

        // And turn the neopixels red
        strip.fill(RED_MED, 0);
        strip.fill(RED_HIGH, pixel_index, 5);
        strip.show();  // Update NeoPixel strip
    }
    else {
        digitalWrite(LED, HIGH);

        // And turn the neopixels red
        strip.fill(RED_MED, 0);

        if (pixel_index + 5 >= LED_COUNT) {
            going = 0;
        }
        else if (pixel_index <= 0) {
            going = 1;
        }

        if (going) {
            strip.fill(RED_HIGH, pixel_index, 5);              
            pixel_index = pixel_index + 1;
        }
        else {
            strip.fill(RED_HIGH, pixel_index, 5);
            pixel_index = pixel_index - 1;
        }
    }
    
    strip.show();  // Update NeoPixel strip

    elapsed_time = millis() - start_time;

    if (elapsed_time < 100) {
        delay(100 - elapsed_time);
    }
}
