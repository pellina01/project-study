#include <Wire.h>
#define SensorPinph 0   //pH meter Analog output to Arduino Analog Input 0
#define SensorPinturb 1 //turb meter Analog output to Arduino Analog Input 1
#define SensorPinDO 2 //DO meter Analog output to Arduino Analog Input 2
#define I2C_SLAVE_ADDRESS 11














#define VREF 5000    //VREF (mv)
#define ADC_RES 1024 //ADC Resolution

//Single-point calibration Mode=0
//Two-point calibration Mode=1
#define TWO_POINT_CALIBRATION 0

#define READ_TEMP (25) //Current water temperature ℃, Or temperature sensor function


//Single point calibration needs to be filled CAL1_V and CAL1_T
#define CAL1_V (785*(5000/1024)) //mv
#define CAL1_T (34.44)   //℃
//Two-point calibration needs to be filled CAL2_V and CAL2_T
//CAL1 High temperature point, CAL2 Low temperature point
#define CAL2_V (786*(5000/1024)) //mv
#define CAL2_T (27.12)   //℃

const uint16_t DO_Table[41] = {
    14460, 14220, 13820, 13440, 13090, 12740, 12420, 12110, 11810, 11530,
    11260, 11010, 10770, 10530, 10300, 10080, 9860, 9660, 9460, 9270,
    9080, 8900, 8730, 8570, 8410, 8250, 8110, 7960, 7820, 7690,
    7560, 7430, 7300, 7180, 7070, 6950, 6840, 6730, 6630, 6530, 6410};

uint8_t Temperaturet;
uint16_t ADC_Raw;
uint16_t ADC_Voltage;
uint16_t DO;

int16_t readDO(uint32_t voltage_mv, uint8_t temperature_c)
{
#if TWO_POINT_CALIBRATION == 0
  uint16_t V_saturation = (uint32_t)CAL1_V + (uint32_t)35 * temperature_c - (uint32_t)CAL1_T * 35;
  return (voltage_mv * DO_Table[temperature_c] / V_saturation);
#else
  uint16_t V_saturation = (int16_t)((int8_t)temperature_c - CAL2_T) * ((uint16_t)CAL1_V - CAL2_V) / ((uint8_t)CAL1_T - CAL2_T) + CAL2_V;
  return (voltage_mv * DO_Table[temperature_c] / V_saturation);
#endif
}













String sensor;
int response;

void setup()
{
  Serial.begin(9600);
  Wire.begin(I2C_SLAVE_ADDRESS); // join i2c bus with address #11
  Wire.onRequest(requestEvent);  // register event
  Wire.onReceive(receiveEvents);
  pinMode(13, OUTPUT);
}

void requestEvent() // new code
{ 
  Serial.println("response value: " + (String)response);
  char buffer [16];
  itoa(response, buffer, 10);
  Wire.write(buffer);
  Serial.println("buffer value: " + (String)buffer);
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
  
  Temperaturet = (uint8_t)READ_TEMP;
  ADC_Raw = analogRead(SensorPinDO);
  ADC_Voltage = uint32_t(VREF) * ADC_Raw / ADC_RES;

  Serial.print("Temperaturet:\t" + String(Temperaturet) + "\t");
  Serial.print("ADC RAW:\t" + String(ADC_Raw) + "\t");
  Serial.print("ADC Voltage:\t" + String(ADC_Voltage) + "\t");
  Serial.println("DO:\t" + String(readDO(ADC_Voltage, Temperaturet)) + "\t");




  return analogRead(SensorPinDO);

}
int tb_raw()
{
  return analogRead(SensorPinturb);
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
  return 1234567812345678;
}
int dummy4()
{
  return 1234567891234567891;
}

void loop(){}