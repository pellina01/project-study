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
  int request;
  while (Wire.available())
  {
    int number = Wire.read();
    request = number;
  }

  switch(request)
  {
    case 1:
      response = ph_raw();
      break;
    case 2:
      response = tb_raw();
      break;
    case 3:
      response = do_raw();
      break;
    case 4:
      response = relay_on();
      break;
    case 5:
      response = relay_off();
      break;
    case 6:
      response = dummy();
      break;
    case 7:
      response = dummy2();
      break;
    case 8:
      response = dummy3();
      break;
    case 9:
      response = dummy4();
      break;
  }

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
int dummy()
{
  return 1234;
}
int dummy2()
{
  return 12345678;
}
int dummy3()
{
  return 12345678912345678;
}
int dummy4()
{
  return 1234567891234567891;
}

void loop(){}