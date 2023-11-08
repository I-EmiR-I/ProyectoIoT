#include <TinyGPS++.h>
#include <SoftwareSerial.h>
#include "ThingSpeak.h"
#include <ESP8266WiFi.h>

static const int RX = D6, TX = D7;
static const uint32_t GPSBaud = 9600;

const char* ssid = "";  // SSID of your WiFi
const char* password = "";  // Password of your WiFi
unsigned long ch_no = 151231;  // Replace with Thingspeak Channel number
const char* write_api = "API KEY";  // Replace with Thingspeak write API

//db connection
const char* host = "192.168.1.8";// IP server, obtained with 'ipconfig' in command shell
const int port = 80;// server port, configured in xampp for Apache server, default is: 80

const int watchdog = 5000;// watchdog frequency, reconnect timeout
unsigned long previousMillis = millis();
int c = 0;// the data


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
    
    //send data to database
    unsigned long currentMillis = millis();
  if(currentMillis - previousMillis > watchdog){
    previousMillis = currentMillis;
    WiFiClient client;// creating the client

    // checking if we can connect to the server
    if(!client.connect(host, port)){
      Serial.println("Fail to connect");
      return;
    }

    // Convertir las variables float a cadenas (String)
    
    String strVariable1 = String(latitude); 
    String strVariable2 = String(longitude);
    
    Serial.println(strVariable1);
    // building our url according our database
    String url = "http://localhost/DB/indexGPS.php?Datos1=" + strVariable1 + "&Datos2=" + strVariable2;

    url += c;

    //Print data to the server that a client is connected to
    client.print(String("GET ") + url + " HTTP/1.1\r\n" +
                "Host: " + host + "\r\n" +
                "Connection: close\r\n\r\n");

    // if watchdog timeout, the client is stopped
    unsigned long timeout = millis();
    while(client.available() == 0){
      if(millis() - timeout > 5000){
        Serial.println(">>> Client Timeout !");
        client.stop();
        return;
      }
    }

    //Read reply from the server
    while(client.available()){
      String line = client.readStringUntil('\r');
      Serial.print(line);
    }
  }

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
