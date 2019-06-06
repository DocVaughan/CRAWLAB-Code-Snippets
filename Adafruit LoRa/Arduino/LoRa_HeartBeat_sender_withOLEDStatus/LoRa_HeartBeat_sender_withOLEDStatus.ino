/* ----------------------------------------------------------------------------

LoRa_HeartBeat_receiver.ino

Arduino sketch to send heartbeat messages, then receive an acknowledgement 
of their receipt. The status is printed to the Serial Monitor and displayed
on a SSD1306 OLED feather

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
#include <Adafruit_GFX.h>
#include <Adafruit_SSD1306.h>

Adafruit_SSD1306 display = Adafruit_SSD1306(128, 32, &Wire);

// OLED FeatherWing buttons map to different pins depending on board:
#if defined(ESP8266)
  #define BUTTON_A  0
  #define BUTTON_B 16
  #define BUTTON_C  2
#elif defined(ESP32)
  #define BUTTON_A 15
  #define BUTTON_B 32
  #define BUTTON_C 14
#elif defined(ARDUINO_STM32_FEATHER)
  #define BUTTON_A PA15
  #define BUTTON_B PC7
  #define BUTTON_C PC5
#elif defined(TEENSYDUINO)
  #define BUTTON_A  4
  #define BUTTON_B  3
  #define BUTTON_C  8
#elif defined(ARDUINO_FEATHER52832)
  #define BUTTON_A 31
  #define BUTTON_B 30
  #define BUTTON_C 27
#else // 32u4, M0, M4, nrf52840 and 328p
  #define BUTTON_A  9
  #define BUTTON_B  6
  #define BUTTON_C  5
#endif



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

// Blinky on receipt
#define LED 13

void setup()
{
  pinMode(LED, OUTPUT);
  pinMode(RFM95_RST, OUTPUT);
  digitalWrite(RFM95_RST, HIGH);

  Serial.begin(115200);

  // Wait for the serial monitor to open
  // Be sure to comment this out in application
//  while (!Serial) {
//    delay(1);
//  }
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

  // Now, finish the set up the OLED
  display.begin(SSD1306_SWITCHCAPVCC, 0x3C); // Address 0x3C for 128x32
  
  // Clear the display buffer.
  display.clearDisplay();
  display.display();

  // Set up the OLED feather's onboard buttons
  pinMode(BUTTON_A, INPUT_PULLUP);
  pinMode(BUTTON_B, INPUT_PULLUP);
  pinMode(BUTTON_C, INPUT_PULLUP);

  // Set up text display
  display.setTextSize(1);
  display.setTextColor(WHITE);
  display.setCursor(0,0);

  display.println("Display and Radio \nInitialized");
  display.setCursor(0,0);
  display.display(); // actually display all of the above
  
  delay(1000); // Show that for one second

  // Then, clear the display buffer.
  display.clearDisplay();
  display.display();
}

void loop() {
    const uint8_t HEARTBEAT_MESSAGE[] = "$ULheartbeat";
    const char ACKNOWLEDGE_MESSAGE[] = "$UL_ACK";
    const int ACKNOWLEDGE_MESSAGE_LENGTH = sizeof(ACKNOWLEDGE_MESSAGE) - 1;

    unsigned long start_time;
    unsigned long elapsed_time;
    start_time = millis();
    
    rf95.send(HEARTBEAT_MESSAGE, sizeof(HEARTBEAT_MESSAGE));
    display.println("Heartbeat: *");

    // Display these headings too, so it seems only the number changes
    display.setCursor(0,10);
    display.println("Acknowledged: "); 
    display.setCursor(0,20);
    display.print("RSSI: ");
    display.setCursor(0,0);
    display.display(); // actually display all of the above
    
    rf95.waitPacketSent();
    digitalWrite(LED, LOW);
    display.clearDisplay();
    display.println("Heartbeat:  "); // Clear the sending message once sent
    
    // Display these headings too, so it seems only the number changes
    display.setCursor(0,10);
    display.println("Acknowledged: "); 
    display.setCursor(0,20);
    display.print("RSSI: ");
    display.display(); // actually display all of the above
    display.setCursor(0,10);
    
    // Now, check for the acknowledgement of it
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
            Serial.print("RSSI: ");
            Serial.println(rf95.lastRssi(), DEC);

            // Compare the message received with the ACKNOWLEDGE_MESSAGE expected
            if (strncmp((char*)buf, ACKNOWLEDGE_MESSAGE, ACKNOWLEDGE_MESSAGE_LENGTH) == 0) {
                Serial.println("Heartbeat acknowledged.");

                display.println("Acknowledged: :)"); // Clear the sending message once sent
                display.setCursor(0,20);
                display.print("RSSI: ");
                display.println(rf95.lastRssi(), DEC);
                display.display();
            }
            else {
                Serial.println("Message was not an acknowledgement.");
                display.println("Acknowledged: :/"); // Clear the sending message once sent
                display.setCursor(0,20);
                display.print("RSSI: ");
                display.println(rf95.lastRssi(), DEC);
                display.display();
            }
        }
    }
    else {
        Serial.println("Received nothing.");
        display.println("Acknowledged: :("); // Clear the sending message once sent
        display.setCursor(0,20);
        display.println("RSSI: ");
        display.display();
    }

    
    elapsed_time = millis() - start_time;

    if (elapsed_time < 500) {
        delay(500 - elapsed_time);
    }
    
    display.clearDisplay();
    display.setCursor(0,0);
}
