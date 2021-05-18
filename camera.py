import picamera
import requests
from PIL import Image
import RPi.GPIO as GPIO
from time import sleep
import json
from os.path import join, dirname
from os import environ
from watson_developer_cloud import VisualRecognitionV3

visual_recognition = VisualRecognitionV3('2016-05-20', api_key='6ccb2135cb0de39c10a64b54ee6280e2aa2f8678')

LED1 = 4
LED2 = 18
LED3 = 22
BTN = 17

ON = GPIO.HIGH
OFF = GPIO.LOW

def setup():	
	GPIO.setmode(GPIO.BCM)		# Numbers GPIOs by physical location
	GPIO.setup(LED1, GPIO.OUT)	# Set LedPin's mode is output
	GPIO.setup(LED2, GPIO.OUT)
	GPIO.setup(BTN, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
	GPIO.output(LED1, OFF)		# Set LedPin high(+3.3V) to off led
	GPIO.output(LED2, OFF)
	GPIO.output(LED3, OFF)
	
def destroy():
	GPIO.output(LED1, OFF)
	GPIO.output(LED2, OFF)
	GPIO.output(LED3, OFF)
	GPIO.cleanup()			# Release resource
	
def camera():
	GPIO.output(LED2, ON)
	GPIO.output(LED3, OFF)
	camera = picamera.PiCamera()
	camera.resolution = (3280, 2464)
	camera.capture('image.jpeg')
	img = Image.open('image.jpeg').rotate(270)
	img.save('image.jpeg')
	fileIn = open('image.jpeg', 'rb').read()
	print(json.dumps(visual_recognition.classify(images_url="https://www.ibm.com/ibm/ginni/images/ginni_bio_780x981_v4_03162016.jpg"), indent=2))
	#r = requests.post("http://52.15.34.99:8081", data={'content': fileIn, 'name': "ocr.jpeg"})
	print("image taken")
	camera.close()
	GPIO.output(LED2, OFF)
	GPIO.output(LED3, ON)

def loop():
	while True:
		btnState = GPIO.input(BTN)
		GPIO.output(LED1, ON)
		if btnState == 0:
			print("taking image...")
			camera()

if __name__ == '__main__':		# Program start from here
	setup()
	try:
		loop()
	except KeyboardInterrupt:	# When 'Ctrl+C' is pressed, the child program destroy() will be  executed.
		destroy()
