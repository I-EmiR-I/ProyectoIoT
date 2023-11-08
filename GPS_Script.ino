#include <TinyGPS++.h>
#include <SoftwareSerial.h>
#include "ThingSpeak.h"
#include <ESP8266WiFi.h>

static const int RX = D6, TX = D7;
static const uint32_t GPSBaud = 9600;

const char* ssid = "wifi name";  // SSID of your WiFi
const char* password = "password";  // Password of your WiFi
unsigned long ch_no = 11233123;  // Replace with Thingspeak Channel number
const char* write_api = "API KEY";  // Replace with Thingspeak write API

TinyGPSPlus gps;
WiFiClient client;
WiFiServer server(80);
SoftwareSerial soft(RX, TX);
String latitude_data;
String longitude_data;

void setup() {
  Serial.begin(115200);
  soft.begin(GPSBaud);
  WiFi.begin(ssid, password);
  server.begin();

  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.println("WiFi connecting...");
  }

  Serial.println("WiFi connected");
  Serial.print("Local IP: ");
  Serial.println(WiFi.localIP());
  ThingSpeak.begin(client);
}

void loop() {
  while (soft.available() > 0)
    if (gps.encode(soft.read())) {
      displaydata();
      displaywebpage();
    }

  if (millis() > 5000 && gps.charsProcessed() < 10) {
    Serial.println("GPS Connection Error!!");
    while (true);
  }
}

void displaydata() {
  if (gps.location.isValid()) {
    double latitude = gps.location.lat();
    double longitude = gps.location.lng();
    latitude_data = String(latitude, 6);
    longitude_data = String(longitude, 6);
    ThingSpeak.setField(1, latitude_data);
    ThingSpeak.setField(2, longitude_data);
    ThingSpeak.writeFields(ch_no, write_api);
    delay(20000);
  } else {
    Serial.println("Data error!!!");
  }
}

void displaywebpage() {
  WiFiClient client = server.available();
  if (!client) {
    return;
  }

  String page = "<html><center><p><h1>Real Time Vehicle Tracking using IoT</h1>";
  page += "<a style='color: RED; font-size: 125%;' href='http://maps.google.com/maps?&z=15&mrt=yp&t=k&q=";
  page += latitude_data;
  page += "+";
  page += longitude_data;
  page += "'>Click here For Live Location</a></p></center></html>";

  client.print("HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n\r\n");
  client.print(page);

  delay(100);
}
