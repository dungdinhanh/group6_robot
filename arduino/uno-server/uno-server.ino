#include "DHT.h"
#include <string.h>
#include <stdio.h>
#include <stdlib.h>
#include <ctype.h>
#include <SoftwareSerial.h>

#define MAX_DATA 200
#define DHTPIN 7     // what digital pin we're connected to
#define DHTTYPE DHT22   
#define BUFFER_SIZE 64//This will prevent buffer overruns.
DHT dht(DHTPIN, DHTTYPE);
/*Buffer setup*/
char inData[BUFFER_SIZE];//This is a character buffer where the data sent by the python script will go.
//char inChar=-1;//Initialie the first character as nothing
/*blutooth setup*/
SoftwareSerial serial_connection(10, 11);//Create a serial connection with TX and RX on these pins

void setup() {
  Serial.begin(9600);
  serial_connection.begin(9600);//Initialize communications with the bluetooth module
  serial_connection.println("Ready!!!");//Send something to just start comms. This will never be seen.
  Serial.println("Started");//Tell the serial monitor that the sketch has started.
  dht.begin();
}

void loop() {
  // delay for preparing the sensor
 delay(2000);
 /*sending*/
// char sending[MAX_DATA];
// sprintf(sending, "{humidity: %f, temprature : %f}", hum(), temp());
String sending = "";
sending += hum();
sending += " - ";
sending += temp();
serial_connection.print(sending);
Serial.println(sending);
// serial_connection.print("{ humiditi: ");/*sending humidity data*/
// serial_connection.println(hum());
// serial_connection.print("temprature: ");
// serial_connection.println(temp());
// serial_connection.println("}");/*sending temp data*/
 /*receiving*/
 int i=0;
 byte byte_count=serial_connection.available();//This gets the number of bytes that were sent by the python script
    for(i=0;i<byte_count;i++)//Handle the number of incoming bytes
    {
    inData[i]=serial_connection.read();
    }
    byte_count = 0;
    Serial.println(inData);
    //Print to the monitor what was detected
}
/* read DHT22 sensor */
float hum(){
  float h = dht.readHumidity();
  if (isnan(h)) {
  Serial.println("Failed to read from DHT sensor!");
    }
  return h;
}
float temp(){
  float t = dht.readTemperature();
  if (isnan(t)) {
  Serial.println("Failed to read from DHT sensor!");
    }
  return t;
}


