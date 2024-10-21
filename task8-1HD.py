import bluetooth
import RPi.GPIO as GPIO
import time

# Setup GPIO for LED
LED_PIN = 18  # Example GPIO pin connected to the LED
GPIO.setmode(GPIO.BCM)
GPIO.setup(LED_PIN, GPIO.OUT)
pwm = GPIO.PWM(LED_PIN, 1000)  # PWM for brightness control
pwm.start(0)

# Function to map sensor value to LED brightness
def set_led_brightness(light_level):
    brightness = int(light_level / 100 * 100)  # Map light level (0-100 lux) to 0-100%
    pwm.ChangeDutyCycle(brightness)

# Bluetooth setup
server_sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
server_sock.bind(("", bluetooth.PORT_ANY))
server_sock.listen(1)

client_sock, address = server_sock.accept()
print("Accepted connection from", address)

try:
    while True:
        data = client_sock.recv(1024)
        if data:
            light_level = float(data)  # Convert received data to float
            print("Received light level:", light_level)
            set_led_brightness(light_level)  # Adjust LED brightness
        time.sleep(0.5)

except KeyboardInterrupt:
    pass

finally:
    pwm.stop()
    GPIO.cleanup()
    client_sock.close()
    server_sock.close()
