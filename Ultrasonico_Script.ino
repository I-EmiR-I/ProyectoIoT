#include <ESP8266WiFi.h>


const char* ssid = "2";// SSID, the name of your WiFi connection
const char* password = "";// password of the WiFi
const char* host = "ipv4 address";// IP server, obtained with 'ipconfig' in command shell
const int port = 80;// server port, configured in xampp for Apache server, default is: 80

const int watchdog = 5000;// watchdog frequency, reconnect timeout
unsigned long previousMillis = millis();
int c = 0;// the data

//sensor ultrasonico
const int trigPin = D5;
const int echoPin = D6;
const int ledPin = D7;  // Pin para el LED

long duration;
int distance;



float Variable1 = 0;
float Variable2 = 0;

void setup() {
  //Sensor de movimiento
  pinMode(trigPin, OUTPUT);  // Configura el trigPin como salida
  pinMode(echoPin, INPUT);   // Configura el echoPin como entrada
  pinMode(ledPin, OUTPUT);   // Configura el ledPin como salida
  Serial.begin(9600);       // Inicia la comunicación serial


  
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
// Clears the trigPin
  digitalWrite(trigPin, LOW);
  delayMicroseconds(2);

  // Sets the trigPin on HIGH state for 10 microseconds
  digitalWrite(trigPin, HIGH);
  delayMicroseconds(10);
  digitalWrite(trigPin, LOW);

  // Reads the echoPin, returns the sound wave travel time in microseconds
  duration = pulseIn(echoPin, HIGH);

  // Calculating the distance
  distance = duration * 0.034 / 2;

  // Prints the distance on the Serial Monitor
  Serial.print("Distance: ");
  Serial.println(distance);

  // Check if the distance is less than 20 cm
  if (distance < 20) {
    digitalWrite(ledPin, HIGH);  // Enciende el LED
  } else {
    digitalWrite(ledPin, LOW);   // Apaga el LED
  }

  delay(2000);



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
    
    String strVariable1 = String(distance); // 2 indica el número de decimales
    
    
    Serial.println(strVariable1);
    // building our url according our database
    String url = "http://localhost/DB/index.php?Datos=" + strVariable1;

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
