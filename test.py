import picamera
import requests
from PIL import Image
from time import sleep

camera = picamera.PiCamera() 
camera.resolution = (820, 616)
camera.color_effects = (128,128)
camera.shutter_speed = 6000000
camera.sharpness = 100

try:
	camera.start_preview()
	print("started")
	key = input()
	if key == 1:
		print("key press")
		camera.capture('ocr.jpeg')
		img = Image.open('ocr.jpeg').rotate(270)
		img.save('ocr.jpeg')
		#$fileIn = open('ocr.jpeg', 'rb').read()
		#r = requests.post("http://www.techundertwenty.com/save.php", data={'content': fileIn, 'name': "ocr.jpeg"})
		#print(r.text)
	camera.stop_preview()
except KeyboardInterrupt:
	print("end")
	camera.stop_preview()
	camera.close()
finally:
	camera.close()
