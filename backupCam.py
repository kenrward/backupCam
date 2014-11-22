# -*- coding: utf-8 -*-
# Modified code from http://jeremyblythe.blogspot.co.uk/2013/03/raspberry-pi-parking-camera-with.html
# to use SainSmart Ultrasonic ranging module (HC - SR04)
# and Raspi Camera from Element 14.  

import RPi.GPIO as GPIO
import time
from time import sleep
import pygame
import picamera
import os
GPIO.setmode(GPIO.BCM)

trig_pin = 23	# orange
echo_pin = 24	# red

BLACK = 0,0,0
GREEN = 0,255,0
RED = 255,0,0

GPIO.setup(trig_pin, GPIO.OUT)
GPIO.setup(echo_pin, GPIO.IN)
	

def getDistance():
	GPIO.output(trig_pin, False)
	print("Waiting for sensor to settle")
	time.sleep(2)
	GPIO.output(trig_pin, True)
	time.sleep(0.00001)
	GPIO.output(trig_pin, False)

	while GPIO.input(echo_pin)==0:
		pulse_start = time.time()

	while GPIO.input(echo_pin)==1:
		pulse_end = time.time()

	pulse_duration = pulse_end - pulse_start

	distance = (pulse_duration * 13514.17)/2 #inches
	print(distance)
	inch = int(round(distance))
	print(inch)
	return(inch)
	
	
pygame.init()
pygame.mouse.set_visible(False)
lcd = pygame.display.set_mode((176,220))
lcd.fill(BLACK)
pygame.display.update()


size = (176,144)

cam = picamera.PiCamera()
cam.vflip = False
cam.hflip = False
cam.brightness = 60

font_big = pygame.font.Font(None, 50)
surf = pygame.Surface(size)

cam.start_preview()
sleep(0.5)
cam.capture('image.gif', format='gif', resize=(size))
#cam.stop_preview()

img= pygame.image.load('image.gif')
lcd.blit(img, (0,0))
pygame.display.update()

font_big = pygame.font.Font(None, 50)
surf = pygame.Surface(size)
try:
	while True:
		lcd.fill(BLACK)
		cam.start_preview()
		sleep(0.5)
		cam.capture('image.gif', format='gif', resize=(size))
		img= pygame.image.load('image.gif')
		lcd.blit(img, (0,0))
		#pygame.display.update()


		dist = getDistance()
		colour = GREEN
		if dist < 4:
			colour = RED
			text_surface = font_big.render('STOP', True, colour)
			rect = text_surface.get_rect(center=(88,72))
			lcd.blit(text_surface, rect)

		if dist < 140:
			pygame.draw.circle(lcd, colour, (88,72), (150-dist)/2, 3)
		 
		text_surface = font_big.render('%din'%dist, True, colour)
		rect = text_surface.get_rect(center=(88,180))
		lcd.blit(text_surface, rect)

		pygame.display.update()

	sleep(8)
	pygame.quit()

except KeyboardInterrupt:
	GPIO.cleanup()
	pygame.quit()
