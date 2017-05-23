# External module imports
import RPi.GPIO as GPIO
import time
import os

# Pin Definitons:
ledPin = 10
butPin = 8
radarPin = 12
relay1Pin = 37
relay2Pin = 35
relay3Pin = 33
relay4Pin = 31

GPIO.setmode(GPIO.BOARD)

GPIO.setup(ledPin, GPIO.OUT)
GPIO.setup(relay1Pin, GPIO.OUT)
GPIO.setup(relay2Pin, GPIO.OUT)
GPIO.setup(relay3Pin, GPIO.OUT)
GPIO.setup(relay4Pin, GPIO.OUT)

GPIO.setup(radarPin, GPIO.IN)
GPIO.setup(butPin, GPIO.IN, pull_up_down=GPIO.PUD_UP) # Button pin set as input w/ pull-up
 
# initial states
GPIO.output(ledPin, GPIO.HIGH)
GPIO.output(relay1Pin, GPIO.HIGH)
GPIO.output(relay2Pin, GPIO.HIGH)
GPIO.output(relay3Pin, GPIO.HIGH)
GPIO.output(relay4Pin, GPIO.HIGH)


last_time_camera_wakeup = time.time()

def keep_camera_alive():
	global last_time_camera_wakeup
	if time.time()-last_time_camera_wakeup > 10:
		os.system("gphoto2 --get-config=/main/status/batterylevel")
		last_time_camera_wakeup = time.time()

def count_down_button():
	for i in range(20):
		GPIO.output(ledPin, GPIO.HIGH)
		time.sleep(0.075)
		GPIO.output(ledPin, GPIO.LOW)
		time.sleep(0.075)

def count_down_relais():
	GPIO.output(relay1Pin, GPIO.LOW)
	time.sleep(1)
	GPIO.output(relay1Pin, GPIO.HIGH)
	GPIO.output(relay2Pin, GPIO.LOW)
	time.sleep(1)
	GPIO.output(relay2Pin, GPIO.HIGH)
	GPIO.output(relay3Pin, GPIO.LOW)
	time.sleep(1)
	GPIO.output(relay3Pin, GPIO.HIGH)

print("Here we go! Press CTRL+C to exit")
try:
	while 1:

		# check radar sensor
		if GPIO.input(radarPin):			
			GPIO.output(relay4Pin, GPIO.HIGH)
		else:
			GPIO.output(relay4Pin, GPIO.LOW)
		
		#GPIO.output(relay4Pin, GPIO.LOW)

		keep_camera_alive()
	
		if GPIO.input(butPin):
 
			count_down_relais()

			os.system("gphoto2 --capture-image-and-download  --filename \"%Y-%m-%d-%H-%M-%S.jpg\"")

			GPIO.output(ledPin, GPIO.HIGH)

			os.system("sudo killall fbi")
			os.system("sudo fbi -noverbose -a -d /dev/fb0 $(ls -1t | head -1) -T 1")

except KeyboardInterrupt: # If CTRL+C is pressed, exit cleanly:
	GPIO.cleanup() # cleanup all GPIO
