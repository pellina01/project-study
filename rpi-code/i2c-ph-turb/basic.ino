#include <Wire.h>
#define SensorPinph 0   //pH meter Analog output to Arduino Analog Input 0
#define SensorPinturb 1 //turb meter Analog output to Arduino Analog Input 1
#define SensorPinDO 2 //DO meter Analog output to Arduino Analog Input 2
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
    response = ph_accumulated();
  }
  if(request == "2") // if requested is raw tb
  {
    response = tb_raw();
  }
  if(request == "3") // if requested is raw do
  {
    response = do_raw();
  }
  if(request == "4") // if requested is on relay data
  {
    response = relay_on();
  }
  if(request == "5") // if requested is off relay data
  {
    response = relay_off();
  }
  if(request == "6") // if requested is raw ph
  {
    response = ph_raw();
  }
}


int ph_accumulated()
{
    int accumulator = 0;
    for(int i = 1; i <= 10; i++){
        accumulator += analogRead(SensorPinph);
    }
    return accumulator;
}
int ph_raw()
{
    return analogRead(SensorPinph);
}
int do_raw()
{
  return analogRead(SensorPinturb);
}
int tb_raw()
{
  return analogRead(SensorPinDO);
}
int relay_off()
{
  digitalWrite(13, LOW);
  return 0;
}

int relay_on()
{
  digitalWrite(13, HIGH);
  return 1;
}


void loop(){}