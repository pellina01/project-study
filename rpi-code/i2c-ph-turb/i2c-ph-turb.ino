#include <Wire.h>
#define SensorPinph 0   //pH meter Analog output to Arduino Analog Input 0
#define SensorPinturb 1 //turb meter Analog output to Arduino Analog Input 0
#define I2C_SLAVE_ADDRESS 11

String sensor;
float response;

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
void loop()
{
}

// void requestEvent()
// { // if request send from raspi, we will respond with "ek"
//   float response;
//   char buffer[16];
//   if (sensor == "ph")
//   {
//     response = ph();
//   }
//   else if (sensor == "turbidity")
//   {
//     response = turb();
//   }
//   else if (sensor == "do")
//   {
//     response = doxy();
//   }
//   else if(sensor == "relay_on")
//   {
//     response = relay_on();
//   }
//   else if(sensor == "relay_off")
//   {
//     response = relay_off();
//   }
//   dtostrf(response, 13, 2, buffer);
//   Wire.write(buffer);
//   Serial.println("responsed");
// }



// void receiveEvents(int numBytes) // if some data has been recieved from raspi
// {
//   String request;
//   while (Wire.available())
//   {
//     int number = Wire.read();
//     request = (char)number;
//     Serial.println(request);
//   }
//   if (request == "1")
//   {
//     sensor = "ph";
//   }
//   if (request == "2")
//   {
//     sensor = "turbidity";
//   }
//   if (request == "3")
//   {
//     sensor = "do";
//   }
  
//   if(request == "4"){
//     sensor = "relay_on";
//   }
//   if(request == "5"){
//     sensor = "relay_off";
//   }
// }


void requestEvent() // new code
{ // if request send from raspi, we will respond with "ek"
  // char buffer[16]; // new code
  // dtostrf(response, 13, 2, buffer);

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
  if (request == "1") // if requested is pH data
  {
    response = ph();
  }
  if (request == "2") // if requested is TB data
  {
    response = turb();
  }
  if (request == "3") // if requested is DO data
  {
    response = doxy();
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
  if(request == "7") // if requested is raw do
  {
    response = do_raw();
  }
  if(request == "8") // if requested is raw tb
    response = tb_raw();
  }
}

float ph()
{
  digitalWrite(12, HIGH);
  delay(1000);
  unsigned long int avgValue; //Store the average value of the sensor feedback
  float b;
  int buf[10], temp;

  for (int i = 0; i < 10; i++) //Get 10 sample value from the sensor for smooth the value
  {
    buf[i] = analogRead(SensorPinph);
    delay(10);
  }
  for (int i = 0; i < 9; i++) //sort the analog from small to large
  {
    for (int j = i + 1; j < 10; j++)
    {
      if (buf[i] > buf[j])
      {
        temp = buf[i];
        buf[i] = buf[j];
        buf[j] = temp;
      }
    }
  }
  avgValue = 0;
  for (int i = 2; i < 8; i++)
  { //take the average value of 6 center sample
    avgValue += buf[i];
  }

  float phValue = (float)avgValue * 5.0 / 1024 / 6; //convert the analog into millivolt
  phValue = (13.96 * phValue - 19.92);              //convert the millivolt into pH value
  return (phValue);
}

float turb()
{
  float ntu;
  float volt1;
  int sensorValue = analogRead(SensorPinturb); // read the input on analog pin 0:
  volt1 = sensorValue * (5.0 / 1024.0);        // Convert the analog reading (which goes from 0 - 1023) to a voltage (0 - 5V):
  if (volt1 < 2.5)
  {
    ntu = 3000;
  }
  else if (volt1 > 4.19)
  {
    ntu = 10;
  }
  else
  {
    ntu = -1120.4 * pow(volt1, 2) + 5742.3 * volt1 - 4353.8;
  }
  return ntu;
}

float doxy()
{
  digitalWrite(12, LOW);
  delay(1000);
  return (float)analogRead(A2);
  }


float relay_on()
{
  digitalWrite(13, LOW);
  return 1;
}

float relay_off()
{
  digitalWrite(13, HIGH);
  return 0;
}

int ph_raw()
{
  digitalWrite(12, HIGH);
  delay(100);
  return analogRead(SensorPinph);
}

int do_raw()
{
  digitalWrite(12, LOW);
  delay(100);
  return analogRead(A2);
}


int tb_raw()
{
  return analogRead(SensorPinturb);
}