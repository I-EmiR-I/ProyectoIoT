#include <ESP8266WiFi.h>

const char* ssid = "";// SSID, the name of your WiFi connection
const char* password = "";// password of the WiFi
const char* host = "ipv4 address";// IP server, obtained with 'ipconfig' in command shell
const int port = 80;// server port, configured in xampp for Apache server, default is: 80

const int watchdog = 5000;// watchdog frequency, reconnect timeout
unsigned long previousMillis = millis();
int c = 0;// the data

//sensor de movimiento
int LED = 2;          
int SENSOR_OUTPUT_PIN = 5;


float Variable1 = 10.5;
float Variable2 = 20.5;

void setup() {
  //Sensor de movimiento
  pinMode(SENSOR_OUTPUT_PIN, INPUT);  
  pinMode(LED, OUTPUT);           
  Serial.begin(9600);

  
  // put your setup code here, to run once:
  Serial.begin(9600);// initialize the serial port
  Serial.println("Counter\n\n");
  
  WiFi.begin(ssid, password);// initialize the WiFi connection
  
  // checking for unsuccessful connection
  while(WiFi.status() != WL_CONNECTED){
    delay(500);
    Serial.print(".");
  }
  
  // continue after successful connection
  Serial.println("");
  Serial.println("WiFi connected");
  Serial.print("IP address: ");
  Serial.println(WiFi.localIP());
  
  delay(100);
}

void loop() {
  //Sensor de movimiento
  int sensorvalue = digitalRead(SENSOR_OUTPUT_PIN);
  Serial.println(sensorvalue);
  if (sensorvalue== HIGH) {
   digitalWrite(LED, HIGH);
    delay(1);
  }
  else {
    digitalWrite(LED,LOW);
  }


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
    String strVariable1 = String(sensorvalue); // 2 indica el número de decimales

    // building our url according our database
    String url = "http://localhost/DB/index.php?movimientoDetectado=" + strVariable1 + "&embarcacionID=1&idSensor=3";;
    
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
  
  delay(1000);
}
