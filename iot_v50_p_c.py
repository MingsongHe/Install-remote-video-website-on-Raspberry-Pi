#!/home/pi/Desktop
#       utf-8
#       python and Flask
#  	iot_v50.py have login interface
# 	PiCam and UBSCam on Web Server with Flask
#       EMS SUNLIGHT SERVICE IOT TEAM 25-11-2020

import RPi.GPIO as GPIO
import pymysql

import ctypes
from ctypes import *

def get_conn():
    return pymysql.connect(
        host='127.0.0.1',
        user='root',
        password='7013',
        database='wpiot',
        charset= 'utf8'
    )

def query_data(sql):
    conn = get_conn()
    try:
       cursor = conn.cursor(pymysql.cursors.DictCursor)
       cursor.execute(sql)
       return cursor.fetchall()
    finally:
        conn.close()

def insert_or_updata_data(sql):
    conn = get_conn()
    try:
       cursor = conn.cursor()
       cursor.execute(sql)
       conn.commit()
    finally:
        conn.close()

def Motor_Type_A_Drive(aa,bb,cc,dd,step_time,number_of_steps):
   global CamPitch
   CamPitch=1
   import sys
   import time
   StepPins = [aa,bb,cc,dd]

   for pin in StepPins:

     GPIO.setup(pin,GPIO.OUT)
     GPIO.output(pin, False)

   Seq = [[1,0,0,1],
          [1,0,0,0],
          [1,1,0,0],
          [0,1,0,0],
          [0,1,1,0],
          [0,0,1,0],
          [0,0,1,1],
          [0,0,0,1]]
   StepCount = len(Seq)
   StepDir = 1
   if len(sys.argv)>1:
     WaitTime = int(sys.argv[1])/float(1000)
   else:
     WaitTime = step_time/float(1000)

   StepCounter = 0

   Step = number_of_steps
   while Step >= 0:
     if CamPitch == 0:
        Step=-1
     else:
        Step=Step-1

     for pin in range(0, 4):
       xpin = StepPins[pin]
       if Seq[StepCounter][pin]!=0:
         GPIO.output(xpin, True)
       else:
         GPIO.output(xpin, False)

     StepCounter += StepDir

     if (StepCounter>=StepCount):
       StepCounter = 0
     if (StepCounter<0):
       StepCounter = StepCount+StepDir

     time.sleep(WaitTime)
   GPIO.output(12, GPIO.LOW)
   GPIO.output(16, GPIO.LOW)
   GPIO.output(20, GPIO.LOW)
   GPIO.output(21, GPIO.LOW)
  # return None

#from flask import Flask, render_template, Response
#from flask import request
from flask import Flask, render_template, Response, request
app = Flask(__name__)

# Raspberry Pi camera module (requires picamera package)
from camera_pi import Camera #This is for pi camera
#from camera import VideoCamera #This is for all connect camera incloud pi and USB
#from pi_usb_camera_cv2 import VideoCamera_pi, VideoCamera_usb

global CamPitch
global CamRotation
CamPitch=0
CamRotation=0

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

#Create a dictionary called pins to store the pin number, name, and pin state:
pins = {
   22 : {'name' : 'Lamp02', 'state' : GPIO.LOW, 'Language' : '0'},
   27 : {'name' : 'LSpot', 'state' : GPIO.LOW, 'Language' : '1'}
       }
for pin in pins:
   GPIO.setup(pin, GPIO.OUT)
   GPIO.output(pin, GPIO.LOW)

# Set each pin as an output and make it low:
#5,6,13,19 pin is left and right stepper motor control

GPIO.setup(5, GPIO.OUT)
GPIO.output(5, GPIO.LOW)
GPIO.setup(6, GPIO.OUT)
GPIO.output(6, GPIO.LOW)
GPIO.setup(13, GPIO.OUT)
GPIO.output(13, GPIO.LOW)
GPIO.setup(19, GPIO.OUT)
GPIO.output(19, GPIO.LOW)

#18,25,24,23 pin for turn left and turn right stepper motor control
GPIO.setup(18, GPIO.OUT)
GPIO.output(18, GPIO.LOW)
GPIO.setup(25, GPIO.OUT)
GPIO.output(25, GPIO.LOW)
GPIO.setup(24, GPIO.OUT)
GPIO.output(24, GPIO.LOW)
GPIO.setup(23, GPIO.OUT)
GPIO.output(23, GPIO.LOW)
#12,16,20,21 pin for up and down angle stepper motor control
GPIO.setup(12, GPIO.OUT)
GPIO.output(12, GPIO.LOW)
GPIO.setup(16, GPIO.OUT)
GPIO.output(16, GPIO.LOW)
GPIO.setup(20, GPIO.OUT)
GPIO.output(20, GPIO.LOW)
GPIO.setup(21, GPIO.OUT)
GPIO.output(21, GPIO.LOW)

GPIO.setup(17, GPIO.OUT)
GPIO.output(17, GPIO.LOW)
GPIO.setup(26, GPIO.OUT)
GPIO.output(26, GPIO.LOW)
GPIO.setup(14, GPIO.OUT)
GPIO.output(14, GPIO.LOW)

GPIO.setup(4, GPIO.OUT)
GPIO.output(4, GPIO.LOW)
p = GPIO.PWM(4, 0.5)
p.start(50)
"""
lib = ctypes.cdll.LoadLibrary("./libhaisantts.so")
lib.startHaisanTTS.argtypes=[POINTER(c_char)]
TTS=(c_char * 100)(*bytes("物联网 V5.0",'utf-8'))
cast(TTS, POINTER(c_char))
lib.startHaisanTTS(TTS)
"""
@app.route("/cn")
def index_cn():
   # Put the message dictionary into the template data dictionary:
   message = ""
   templateData = {
      'message' : message,
      }
   # Pass the template data into the template main.html and return it to the user
   return render_template('login_cn.html', **templateData)

@app.route("/us")
def index_us():
   # Put the message dictionary into the template data dictionary:
   message = ""
   templateData = {
      'message' : message,
      }
   # Pass the template data into the template main.html and return it to the user
   return render_template('login_us.html', **templateData)

# The function below is executed when someone requests a URL with the pin number and action in it:

@app.route('/iotcn', methods=['POST'])
def verify_username_and_password_cn():
   sql = "select * from ufq_iot_user_login"
   datas = query_data(sql)

   username = request.form.get("username")
   password = request.form.get("password")

   # Along with the pin dictionary, put the message into the template data d$
   if(datas[0].get('username') == username and datas[0].get('password') == password):
      datetime = datas[0].get('datetime')
      sql = "update ufq_iot_user_login set datetime=NOW() where id=1"
      insert_or_updata_data(sql)

      c_message = "成功登录！您上一次的登录时间是："
      e_message = "Successfully logged in! Your last login time was:"
      templateData = {
      'c_message' : c_message,
      'e_message' : e_message,
      'datetime' : datetime
      }
      return render_template('index_v50_cn.html', **templateData)
   else:
      chinese_message = "用户名或密码错误，按'确定'重新登录!"
      english_message = "The username or password is wrong, press 'OK' to login again!"
      templateData = {
      'chinese_message' : chinese_message,
      'english_message' : english_message
      }
      return render_template('login_cn.html', **templateData)

@app.route('/iotus', methods=['POST'])
def verify_username_and_password_us():
   sql = "select * from ufq_iot_user_login"
   datas = query_data(sql)

   username = request.form.get("username")
   password = request.form.get("password")

   # Along with the pin dictionary, put the message into the template data d$
   if(datas[0].get('username') == username and datas[0].get('password') == password):
      datetime = datas[0].get('datetime')
      sql = "update ufq_iot_user_login set datetime=NOW() where id=1"
      insert_or_updata_data(sql)

      c_message = "***"
      e_message = "Successfully logged in! Your last login time was:"
      templateData = {
      'c_message' : c_message,
      'e_message' : e_message,
      'datetime' : datetime
      }
      return render_template('index_v50_us.html', **templateData)
   else:
      chinese_message = "***"
      english_message = "The username or password is wrong, press 'OK' to login again!"
      templateData = {
      'chinese_message' : chinese_message,
      'english_message' : english_message
      }
      return render_template('login_us.html', **templateData)

@app.route('/text_message', methods=['POST'])
def text_message():
#   import ctypes
#   from ctypes import *
   import sys
   txt_message = request.form.get("txt_message")
   lib = ctypes.cdll.LoadLibrary("./libhaisantts.so")
   lib.startHaisanTTS.argtypes=[POINTER(c_char)]
   TTS=(c_char * 100)(*bytes(txt_message,'utf-8'))
   cast(TTS, POINTER(c_char))
   lib.startHaisanTTS(TTS)

   return "Send text message finish"

@app.route('/lightspoton', methods=['POST'])
def lightspoton():
   GPIO.output(27, GPIO.HIGH)
   return "light spot on finish"

@app.route('/lightspotoff', methods=['POST'])
def lightspotoff():
   GPIO.output(27, GPIO.LOW)
   return "light spot off finish"

@app.route('/lampon', methods=['POST'])
def lampon():
   GPIO.output(22, GPIO.HIGH)
   return "lamp on finish"
@app.route('/lampoff', methods=['POST'])
def lampoff():
   GPIO.output(22, GPIO.LOW)
   return "lamp off finish"
CamRotation
@app.route('/camoff', methods=['POST'])
def camoff():
   global CamPitch
   CamPitch=0
   return "camoff finish"

@app.route('/camup', methods=['POST'])
def camup():
   Motor_Type_A_Drive(12,16,20,21,10,200)

@app.route('/trolleyleftoff', methods=['POST'])
def trolleyleftoff():
   GPIO.output(26, GPIO.LOW)
   return "trolleyleftoff finish"

@app.route('/camleft', methods=['POST'])
def camleft():
   global CamPitch
   CamPitch=1
   import sys
   import time
   StepPins = [25,24,23,18]

   for pin in StepPins:
     print ("Setup pins")
     GPIO.setup(pin,GPIO.OUT)
     GPIO.output(pin, False)

   Seq = [[1,0,0,1],
          [1,0,0,0],
          [1,1,0,0],
          [0,1,0,0],
          [0,1,1,0],
          [0,0,1,0],
          [0,0,1,1],
          [0,0,0,1]]
   StepCount = len(Seq)
   StepDir = 1
   if len(sys.argv)>1:
     WaitTime = int(sys.argv[1])/float(1000)
   else:
     WaitTime = 10/float(1000)

   StepCounter = 0

   Step = 200
   while Step >= 0:
     if CamPitch == 0:
        Step=-1
     else:
        Step=Step-1
     print (StepCounter)
     print (Seq[StepCounter])

     for pin in range(0, 4):
       xpin = StepPins[pin]
       if Seq[StepCounter][pin]!=0:
        # print " Enable GPIO %i" %(xpin)
         GPIO.output(xpin, True)
       else:
         GPIO.output(xpin, False)

     StepCounter += StepDir

     if (StepCounter>=StepCount):
       StepCounter = 0
     if (StepCounter<0):
       StepCounter = StepCount+StepDir

     time.sleep(WaitTime)
   GPIO.output(25, GPIO.LOW)
   GPIO.output(24, GPIO.LOW)
   GPIO.output(23, GPIO.LOW)
   GPIO.output(18, GPIO.LOW)

   return "camera go left finish"

@app.route('/camright', methods=['POST'])
def camright():
   global CamPitch
   CamPitch=1
   import sys
   import time
   StepPins = [18,23,24,25]

   for pin in StepPins:
     print ("Setup pins")
     GPIO.setup(pin,GPIO.OUT)
     GPIO.output(pin, False)

   Seq = [[1,0,0,1],
          [1,0,0,0],
          [1,1,0,0],
          [0,1,0,0],
          [0,1,1,0],
          [0,0,1,0],
          [0,0,1,1],
          [0,0,0,1]]
   StepCount = len(Seq)
   StepDir = 1
   if len(sys.argv)>1:
     WaitTime = int(sys.argv[1])/float(1000)
   else:
     WaitTime = 10/float(1000)

   StepCounter = 0

   Step = 200
   while Step >= 0:
     if CamPitch == 0:
        Step=-1
     else:
        Step=Step-1
     print (StepCounter)
     print (Seq[StepCounter])

     for pin in range(0, 4):
       xpin = StepPins[pin]
       if Seq[StepCounter][pin]!=0:
        # print " Enable GPIO %i" %(xpin)
         GPIO.output(xpin, True)
       else:
         GPIO.output(xpin, False)

     StepCounter += StepDir

     if (StepCounter>=StepCount):
       StepCounter = 0
     if (StepCounter<0):
       StepCounter = StepCount+StepDir

     time.sleep(WaitTime)
   GPIO.output(18, GPIO.LOW)
   GPIO.output(23, GPIO.LOW)
   GPIO.output(24, GPIO.LOW)
   GPIO.output(25, GPIO.LOW)

   return "camera go right finish"

@app.route('/camdown', methods=['POST'])
def camdown():
   Motor_Type_A_Drive(21,20,16,12,10,200)

@app.route('/trolleyoff', methods=['POST'])
def trolleyoff():
   global TrolleyPitch
   TrolleyPitch=0
   GPIO.cleanup(14)
   GPIO.output(26, GPIO.LOW)
   return "trolleyoff finish"

@app.route('/trolleyforward', methods=['POST'])
def trolleyforward():
   import time
   GPIO.setup(14,GPIO.OUT,initial=False)
   p = GPIO.PWM(14, 50)
   p.start(0)
#   time.sleep(1)
   p.ChangeDutyCycle(12.5-5*180/360)
   time.sleep(3)
   p.stop()
   GPIO.cleanup(14)
   return "trolley forward finish"

@app.route('/trolleybackward', methods=['POST'])
def trolleybackward():
   import time
   GPIO.setup(14,GPIO.OUT,initial=False)
   p = GPIO.PWM(14, 50)
   p.start(0)
#   time.sleep(1)
   p.ChangeDutyCycle(7.6-5*360/360)
   time.sleep(3)
   p.stop()
   GPIO.cleanup(14)
   return "trolley backward finish"

@app.route('/trolleyleft', methods=['POST'])
def trolleyleft():
   GPIO.output(26, not GPIO.input(17))

   import sys
   import time
   StepPins = [5,6,13,19]

   # Set all pins as output
   for pin in StepPins:
     print ("Setup pins")
     GPIO.setup(pin,GPIO.OUT)
     GPIO.output(pin, False)

         # Define advanced sequence
         # as shown in manufacturers datasheet
   Seq = [[1,0,0,0],
          [0,0,1,0],
          [0,1,0,0],
          [0,0,0,1],
          [1,0,0,0],
          [0,0,1,0],
          [0,1,0,0],
          [0,0,0,1]]
   StepCount = len(Seq)
   StepDir = -1 # Set to 1 or 2 for clockwise
         # Set to -1 or -2 for anti-clockwise

         # Read wait time from command line
   if len(sys.argv)>1:
      WaitTime = int(sys.argv[1])/float(1000)
   else:
      WaitTime = 3/float(1000)

         # Initialise variables
   StepCounter = 0

         # Start main loop
   Step = 3000
   while Step >= 0:
      if GPIO.input(26) == False:
         Step=-1
      else:
         Step=Step-1
      print (StepCounter)
      print (Seq[StepCounter])

      for pin in range(0, 4):
         xpin = StepPins[pin]
         if Seq[StepCounter][pin]!=0:
           # print " Enable GPIO %i" %(xpin)
            GPIO.output(xpin, True)
         else:
            GPIO.output(xpin, False)

      StepCounter += StepDir

            # If we reach the end of the sequence
            # start again
      if (StepCounter>=StepCount):
        StepCounter = 0
      if (StepCounter<0):
          StepCounter = StepCount+StepDir

               # Wait before moving on
      time.sleep(WaitTime)

   for pin in StepPins:
     print ("Setup pins")
     GPIO.setup(pin,GPIO.OUT)
     GPIO.output(pin, False)
   GPIO.output(26, GPIO.LOW)
   return "trolley go left finish"

@app.route('/trolleyright', methods=['POST'])
def trolleyright():
   GPIO.output(26, not GPIO.input(17))

   import sys
   import time
   StepPins = [5,6,13,19]

         # Set all pins as output
   for pin in StepPins:
     print ("Setup pins")
     GPIO.setup(pin,GPIO.OUT)
     GPIO.output(pin, False)

         # Define advanced sequence
         # as shown in manufacturers datasheet
   Seq = [[1,0,0,0],
          [0,0,1,0],
          [0,1,0,0],
          [0,0,0,1],
          [1,0,0,0],
          [0,0,1,0],
          [0,1,0,0],
          [0,0,0,1]]
   StepCount = len(Seq)
   StepDir = 1 # Set to 1 or 2 for clockwise
            # Set to -1 or -2 for anti-clockwise

         # Read wait time from command line
   if len(sys.argv)>1:
      WaitTime = int(sys.argv[1])/float(1000)
   else:
      WaitTime = 3/float(1000)

         # Initialise variables
   StepCounter = 0

         # Start main loop
   Step = 3000
   while Step >= 0:
      if GPIO.input(26) == False:
         Step=-1
      else:
         Step=Step-1
      print (StepCounter)
      print (Seq[StepCounter])

      for pin in range(0, 4):
         xpin = StepPins[pin]
         if Seq[StepCounter][pin]!=0:
    #        print " Enable GPIO %i" %(xpin)
            GPIO.output(xpin, True)
         else:
            GPIO.output(xpin, False)

      StepCounter += StepDir

            # If we reach the end of the sequence
            # start again
      if (StepCounter>=StepCount):
        StepCounter = 0
      if (StepCounter<0):
          StepCounter = StepCount+StepDir

               # Wait before moving on
      time.sleep(WaitTime)

   for pin in StepPins:
     print ("Setup pins")
     GPIO.setup(pin,GPIO.OUT)
     GPIO.output(pin, False)
   GPIO.output(26, GPIO.LOW)
   return "trolley go right finish"

@app.route('/platformoff', methods=['POST'])
def platformoff():
   GPIO.output(17, GPIO.LOW)
   return "platformoff finish"

@app.route('/platformc', methods=['POST'])
def platformc():
   GPIO.output(17, not GPIO.input(26))

   import sys
   import time
   StepPins = [5,6,13,19]

   for pin in StepPins:
     print ("Setup pins")
     GPIO.setup(pin,GPIO.OUT)
     GPIO.output(pin, False)

   Seq = [[1,0,0,1],
          [1,0,0,0],
          [1,1,0,0],
          [0,1,0,0],
          [0,1,1,0],
          [0,0,1,0],
          [0,0,1,1],
          [0,0,0,1]]
   StepCount = len(Seq)
   StepDir = 1
   if len(sys.argv)>1:
     WaitTime = int(sys.argv[1])/float(1000)
   else:
     WaitTime = 3/float(1000)

   StepCounter = 0

   Step = 20000
   while Step >= 0:
     if GPIO.input(17) == False:
        Step=-1
     else:
        Step=Step-1
        if Step <= 18000 and Step > 17000:
           WaitTime = 1/float(1000)
        if Step <= 17000 and Step > 16000:
           WaitTime = 5/float(1000)
        if Step <= 16000 and Step > 15000:
           WaitTime = 1/float(1000)

     print (StepCounter)
     print (Seq[StepCounter])

     for pin in range(0, 4):
       xpin = StepPins[pin]
       if Seq[StepCounter][pin]!=0:
        # print " Enable GPIO %i" %(xpin)
         GPIO.output(xpin, True)
       else:
         GPIO.output(xpin, False)

     StepCounter += StepDir

     if (StepCounter>=StepCount):
       StepCounter = 0
     if (StepCounter<0):
       StepCounter = StepCount+StepDir

     time.sleep(WaitTime)
   GPIO.output(5, GPIO.LOW)
   GPIO.output(6, GPIO.LOW)
   GPIO.output(13, GPIO.LOW)
   GPIO.output(19, GPIO.LOW)

   GPIO.output(17, GPIO.LOW)
   return "platform turn c finish"

@app.route('/platformcc', methods=['POST'])
def platformcc():
   GPIO.output(17, not GPIO.input(26))

   import sys
   import time
   StepPins = [19,13,6,5]

   for pin in StepPins:
     print ("Setup pins")
     GPIO.setup(pin,GPIO.OUT)
     GPIO.output(pin, False)

   Seq = [[1,0,0,1],
          [1,0,0,0],
          [1,1,0,0],
          [0,1,0,0],
          [0,1,1,0],
          [0,0,1,0],
          [0,0,1,1],
          [0,0,0,1]]
   StepCount = len(Seq)
   StepDir = 1
   if len(sys.argv)>1:
     WaitTime = int(sys.argv[1])/float(1000)
   else:
     WaitTime = 1/float(1000)

   StepCounter = 0

   Step = 5000
   while Step >= 0:
     if GPIO.input(17) == False:
        Step=-1
     else:
        Step=Step-1
     print (StepCounter)
     print (Seq[StepCounter])

     for pin in range(0, 4):
       xpin = StepPins[pin]
       if Seq[StepCounter][pin]!=0:
        # print " Enable GPIO %i" %(xpin)
         GPIO.output(xpin, True)
       else:
         GPIO.output(xpin, False)

     StepCounter += StepDir

     if (StepCounter>=StepCount):
       StepCounter = 0
     if (StepCounter<0):
       StepCounter = StepCount+StepDir

     time.sleep(WaitTime)
   GPIO.output(19, GPIO.LOW)
   GPIO.output(13, GPIO.LOW)
   GPIO.output(6, GPIO.LOW)
   GPIO.output(5, GPIO.LOW)

   GPIO.output(17, GPIO.LOW)
   return "platform turn cc finish"


@app.route('/stop', methods=['POST'])
def stop():

   return "for free,no function"
 
def gen(camera):
    """Video streaming generator function."""
    while True:
        frame = camera.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/video_feed')
def video_feed():
    """Video streaming route. Put this in the src attribute of an img tag."""
    return Response(gen(Camera()),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port =8001, debug=True, threaded=True)
