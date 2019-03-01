#include<BLEDevice.h>
#include<BLEUtils.h>
#include<BLEServer.h>
#include<BLE2902.h>

#define TRIG_PIN 10;
#define ECHO_PIN 12;


#define SERVICE_UUID "";
#define CHARACTERISTIC_UUID "";
#define DEVICE_NAME "CAR_1_FRONT";


double CalcDistance(){
	double result;
	digitalWrite(TRIG_PIN,HIGH);
	delayMicroseconds(100):
	digitalWrite(TRIG_PIN,LOW);
	
	interval=pulseIn(ECHO_PIN,HIGH);
	result= 0.017*interval;
	return result;
}

class serverCallbacks: public BLEServerCallbacks{
	void onConnect(BLEServer *pServer){
		deviceConnected=true;
	}
	
	void onDisConnected(BLEServer *pServer){
		deviceConnected=false;
	}
}
class writeCallbacks: public BLECharacteristicCallbacks{
	void onWrite(BLECharacteristic *bleWriteCharacteristic){
		std::string value =bleWriteCharacterstic->getValue():
	}
}

void setup(){
	pinMode(ECHO_PIN,INPUT):
	pinMode(TRIG_PIN,OUTPUT);
	
}
void loop(){
	if(deviceConnecte){
	
}
}
