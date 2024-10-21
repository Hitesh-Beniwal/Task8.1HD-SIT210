#include <Wire.h>
#include <BH1750.h>
#include <ArduinoBLE.h> // Bluetooth library for Arduino

BH1750 lightMeter;

void setup() {
    Serial.begin(9600);
    
    // Initialize I2C communication for BH1750
    Wire.begin();
    
    // Initialize the BH1750 sensor
    if (!lightMeter.begin(BH1750::CONTINUOUS_HIGH_RES_MODE)) {
        Serial.println("Error initializing BH1750 sensor");
        while (1);
    }
    Serial.println("BH1750 sensor initialized");

    // Initialize Bluetooth
    BLE.begin();
    BLE.setLocalName("SensingSubsystem");
    BLE.advertise();
}

void loop() {
    // Read light intensity from the BH1750 sensor
    float lightLevel = lightMeter.readLightLevel();
    
    // Print light level for debugging
    Serial.print("Light: ");
    Serial.print(lightLevel);
    Serial.println(" lx");

    // Send the light level data over Bluetooth
    BLEDevice central = BLE.central();
    if (central) {
        central.println(lightLevel);  // Send data to Raspberry Pi
    }
    
    delay(500);  // Control update frequency
}
