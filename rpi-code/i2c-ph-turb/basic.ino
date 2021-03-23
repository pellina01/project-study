#include <Wire.h>
#define SensorPinph 0   //pH meter Analog output to Arduino Analog Input 0
#define SensorPinturb 1 //turb meter Analog output to Arduino Analog Input 0
#define I2C_SLAVE_ADDRESS 11

String sensor;
int response;

void setup()
{
  Wire.begin(I2C_SLAVE_ADDRESS); // join i2c bus with address #11
  Wire.onRequest(requestEvent);  // register event
  Wire.onReceive(receiveEvents);

  Serial.begin(9600);
  Serial.println("Ready"); //Test the serial monitor
  pinMode(13, OUTPUT);
  pinMode(12, OUTPUT); // if low, DO on. if High, pH on
}

void requestEvent() // new code
{ 
  char buffer [16];
  itoa(response, buffer, 10);
  Wire.write(buffer);
}


void receiveEvents(int numBytes) // if some data has been recieved from raspi (new code)
{
  String request;
  while (Wire.available())
  {
    int number = Wire.read();
    request = (char)number;
  }
  if(request == "1") // if requested is raw ph
  {
    response = ph_raw();
  }
  if(request == "2") // if requested is raw tb
  {
    response = tb_raw();
  }
  if(request == "3") // if requested is raw do
  {
    response = do_raw();
  }
}


int ph_raw()
{
  digitalWrite(12, HIGH);
  delay(100);
  return analogRead(SensorPinph);
}
int do_raw()
{
  digitalWrite(12, HIGH);
  delay(100);
  return analogRead(SensorPinph);
}
int tb_raw()
{
  digitalWrite(12, HIGH);
  delay(100);
  return analogRead(SensorPinph);
}

void loop(){}