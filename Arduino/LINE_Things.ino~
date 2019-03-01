#include<BLEDevice.h>
#include<BLEUtils.h>
#include<BLEServer.h>
#include<BLE2902.h>

#define TRIG_PIN 13
#define ECHO_PIN 12


#define SERVICE_UUID "431baeda-7a5d-4d39-b5e1-fac297f98427"
#define CHARACTERISTIC_UUID "47395845-5b4a-46d7-b6fa-6a87025e4908"
#define DEVICE_NAME "CAR_1_FRONT"

bool deviceConnected= false;
BLECharacteristic *pCharacteristic;
double CalcDistance(){
	double result,interval;
	digitalWrite(TRIG_PIN,HIGH);
	delayMicroseconds(100);
	digitalWrite(TRIG_PIN,LOW);
	
	interval=pulseIn(ECHO_PIN,HIGH);
	result= 0.017*interval;
	return result;
}

class serverCallbacks: public BLEServerCallbacks{
	void onConnect(BLEServer *pServer){
		deviceConnected=true;
	}
	
	void onDisconnect(BLEServer *pServer){
		deviceConnected=false;
	}
};
class writeCallbacks: public BLECharacteristicCallbacks{
	void onWrite(BLECharacteristic *bleWriteCharacteristic){
		std::string value = bleWriteCharacteristic -> getValue();
	}
};

void setup(){
	Serial.begin(115200);
	pinMode(ECHO_PIN,INPUT);
	pinMode(TRIG_PIN,OUTPUT);
	
	BLEDevice::init(DEVICE_NAME);	
	BLEServer *pServer=BLEDevice:: createServer();
  pServer ->setCallbacks(new serverCallbacks());

	BLEService *pService= pServer ->createService(SERVICE_UUID);
	pCharacteristic = pService -> createCharacteristic(
					CHARACTERISTIC_UUID,
					BLECharacteristic::PROPERTY_NOTIFY |
          BLECharacteristic::PROPERTY_READ
	);
	pCharacteristic -> addDescriptor(new BLE2902());
	
	pService->start();
	pServer->getAdvertising()->start();
	Serial.println("Waiting a client connection to notify...");
}
void loop(){
	delay(1000);
	double dist;
  uint8_t ans;
	if(deviceConnected){
		dist=CalcDistance();
    ans=(uint8_t)dist;
		Serial.print("dist=");
		Serial.println(dist);
		pCharacteristic ->setValue(&ans,1);
		pCharacteristic ->notify();
	}
}
