#!/usr/bin/env python
# coding=utf-8
# author:ksc

import RPi.GPIO as GPIO
import time
import os,sys
import signal   #完整退出

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

pin_btn=15
pin_video_working=4

GPIO.setup(pin_btn, GPIO.IN, pull_up_down=GPIO.PUD_UP)

def handleSIGTERM(signum, frame):
    #cleanup()
    sys.exit()        #raise an exception of type SystemExit

def onPress(channel):
#    time.sleep(2)
#    if GPIO.input(pin_btn) == 0:
    print("stop")
    GPIO.setup(pin_video_working, GPIO.OUT)
    GPIO.output(pin_video_working, GPIO.LOW)
    GPIO.cleanup()                #释放资源，不然下次运行是可能会收到警告
    os.system("sudo fuser -k -n tcp 8001")
    os.system("sudo python /var/www/html/wp-content/themes/start-video.py")
    sys.exit()
time.sleep(0.2)
GPIO.add_event_detect(pin_btn, GPIO.FALLING, bouncetime=300)
GPIO.add_event_callback(pin_btn, onPress)

os.system("sudo python /var/www/html/wp-content/themes/iot_v50_p_c.py")

while True:
    try:
        choice = input("Press Enter,Then input choice: b:Quit ")
        if choice == 'b':
           break
    except KeyboardInterrupt:      #捕获用户是否按了Ctrl + C 组合键。退出程序
        break
GPIO.cleanup()                     #建议在使用RPi.GPIO模块的所有Python程序的最后，都写上这个函数
