#include <Arduino.h>
#include <WiFi.h>

const char* ssid = "Anandita's iPhone";
const char* password = "Anandita";

WiFiServer server(1234);

HardwareSerial nanoSerial(2);

uint8_t buffer[7];
int bufIndex = 0;

void setup() {
  Serial.begin(115200);
  delay(1000);

  Serial.println("=== ESP32 BOOT ===");
  Serial.print("Chip model: "); Serial.println(ESP.getChipModel());
  Serial.print("Free heap: "); Serial.println(ESP.getFreeHeap());

  Serial.println("Starting nanoSerial on pins 16/17 at 9600...");
  nanoSerial.begin(9600, SERIAL_8N1, 16, 17);
  Serial.println("nanoSerial OK");

  Serial.print("Connecting to SSID: ");
  Serial.println(ssid);
  WiFi.begin(ssid, password);

  Serial.print("Connecting...");
  int attempts = 0;
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
    Serial.print("["); Serial.print(WiFi.status()); Serial.print("]");
    attempts++;
    if (attempts > 40) {
      Serial.println("\nFAILED after 20s. Status: " + String(WiFi.status()));
      Serial.println("Restarting ESP32...");
      delay(1000);
      ESP.restart();
    }
  }

  Serial.println("\nConnected!");
  Serial.print("IP: "); Serial.println(WiFi.localIP());
  Serial.print("Signal strength (RSSI): "); Serial.print(WiFi.RSSI()); Serial.println(" dBm");
  Serial.print("Gateway: "); Serial.println(WiFi.gatewayIP());

  server.begin();
  Serial.println("TCP server started on port 1234");
  Serial.println("=== READY — waiting for client ===");
}

void loop() {
  WiFiClient client = server.available();

  if (client) {
    Serial.println(">>> Client connected from: " + client.remoteIP().toString());

    while (client.connected()) {

      while (client.available()) {
        uint8_t b = client.read();
        Serial.print("Byte rx: 0x"); Serial.println(b, HEX);

        if (b == 255) {
          bufIndex = 0;
          Serial.println("--- Start byte detected, resetting buffer ---");
        }

        buffer[bufIndex++] = b;
        Serial.print("bufIndex now: "); Serial.println(bufIndex);

        if (bufIndex == 7) {
          Serial.print("Full packet: ");
          for (int i = 0; i < 7; i++) {
            Serial.print(buffer[i]); Serial.print(" ");
          }
          Serial.println();

          if (buffer[0] == 255 && buffer[6] == 254) {
            Serial.println("Packet VALID — forwarding to Nano");
            nanoSerial.write(buffer, 7);
            Serial.println("Nano write done");
          } else {
            Serial.print("Packet INVALID — buffer[0]=");
            Serial.print(buffer[0]);
            Serial.print(" buffer[6]=");
            Serial.println(buffer[6]);
          }

          bufIndex = 0;
        }
      }
    }

    client.stop();
    Serial.println("<<< Client disconnected");
  }
}