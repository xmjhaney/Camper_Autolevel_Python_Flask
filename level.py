                                                                                                                                                             import random
from flask import jsonify


from flask import Flask, render_template, request

import sys, getopt

sys.path.append('.')
import RTIMU
import os.path
import time
import math

import threading

from gpiozero import LED

# Define each GPIO channel for operating remote control (ie: landing gear)
upch1 = LED(5, False, False)
upch2 = LED(6, False, False)
dnch1 = LED(12, False, False)
dnch2 = LED(13, False, False)

upch1.off()
upch2.off()
dnch1.off()
dnch2.off()

#Read prior calibration file
if (os.path.isfile('./calibration.txt') == True):
    print ("Calibration File exists and will be used")
    calibrate = True
else:
    print ("Calibration File does not exist, will be created when calibration run")
    i_offset = 0
    j_offset = 0
    y_offset = 0
    calibrate = False


SETTINGS_FILE = "RTIMULib"

print("Using settings file " + SETTINGS_FILE + ".ini")
if not os.path.exists(SETTINGS_FILE + ".ini"):
  print("Settings file does not exist, will be created")

s = RTIMU.Settings(SETTINGS_FILE)
imu = RTIMU.RTIMU(s)

print("IMU Name: " + imu.IMUName())

if (not imu.IMUInit()):
    print("IMU Init Failed")
    sys.exit(1)
else:
    print("IMU Init Succeeded")

# this is a good time to set any fusion parameters

imu.setSlerpPower(0.02)
imu.setGyroEnable(True)
imu.setAccelEnable(True)
imu.setCompassEnable(True)

poll_interval = imu.IMUGetPollInterval()
print("Recommended Poll Interval: %dmS\n" % poll_interval)




# Color of displayed legs 0 = black, 1 = green, 2 = orange, 3 = blue
lf = 0
rf = 0
lr = 0
rr = 0

# Mode 0 = Off, 1 = Front, 2 = Passenger, 3 = Driver
m = 0

# Action (TBD)
a = 0

# Update 0 = Off, 1 = On
u = 0

#define roll, pitch, yaw
global i, j, y
i = 0
j = 0
y = 0

#define shutdown parameter
shutdown = False


def unhitch(m):
    global i, i_offset
    hitch = i - i_offset
    if (m == 1):
        dnch1.on()
        dnch2.on()
        while (i - i_offset < (hitch + 1)):
            time.sleep(poll_interval*1.0/1000.0)                      
        dnch1.off()
        dnch2.off()
        myfile = open('unhitch.txt','w')
        myfile.write(str(hitch + 1)+'\n')
        myfile.close()
        
def hitch(m):
    global i, i_offset, lf, rf
    if (m == 1):
        if (os.path.isfile('./unhitch.txt') == True):
            myfile = open('unhitch.txt','r')
            hitch1 = float(myfile.readline())
            myfile.close()            
            if (i - i_offset > hitch1):
                upch1.on()
                upch2.on()
                lf = 2
                rf = 2
                while (i - i_offset > hitch1):
                    time.sleep(poll_interval*1.0/1000.0)               
                upch1.off()
                upch2.off()
            elif (i - i_offset < hitch1):
                dnch1.on()
                dnch2.on()
                lf = 1
                rf = 1 
                while (i - i_offset < hitch1):
                    time.sleep(poll_interval*1.0/1000.0)                              
                dnch1.off()
                dnch2.off()
                
def level_jacks(m):
    
    global i, i_offset, j, j_offset, lf, rf, lr, rr
        
    if (m == 0):
        return
    rf = 0
    lf = 0
    rr = 0
    lr = 0
           
# Lowering Front
    if ((i - i_offset > 0) and (m == 1)):
        upch1.on()
        upch2.on()
        rf = 2
        lf = 2
        while (i - i_offset > 0):
            time.sleep(poll_interval*1.0/1000.0)                      
        upch1.off()
        upch2.off()

# Raising Front
    elif ((i - i_offset < 0) and (m == 1)):
        dnch1.on()
        dnch2.on()
        rf = 1
        lf = 1
        while (i - i_offset < 0):
            time.sleep(poll_interval*1.0/1000.0)                      
        dnch1.off()
        dnch2.off()


# Raising Driver Side
    elif ((j - j_offset > 0) and (m == 3)):
        dnch1.on()
        dnch2.on()
        lf = 1
        lr = 1
        while (j - j_offset > 0):
            time.sleep(poll_interval*1.0/1000.0)                      
        dnch1.off()
        dnch2.off()

# Raising Passenger Side
    elif ((j - j_offset < 0) and (m == 2)):
        dnch1.on()
        dnch2.on()
        rf = 1
        rr = 1
        while (j - j_offset < 0):
            time.sleep(poll_interval*1.0/1000.0)                      
        dnch1.off()
        dnch2.off()               
        
    print("Level")

def get_level():
    global i, j, y, shutdown
#    p_pitch = 0
#    p_roll = 0
#    p_yaw = 0
    while not shutdown:

        if imu.IMURead():
      # x, y, z = imu.getFusionData()
      # print("%f %f %f" % (x,y,z))
            data = imu.getIMUData()
            fusionPose = data["fusionPose"]
            i = math.degrees(fusionPose[0])            
            j = math.degrees(fusionPose[1])
            y = math.degrees(fusionPose[2])
#            print (i,j)
            time.sleep(poll_interval*1.0/1000.0)   

app = Flask(__name__)



@app.route("/",methods=['GET','POST'])
def index(name='index'):
    global m, u, a, lf, rf, lr, rr, i, j, y, i_offset, j_offset, y_offset, calibrate

    if (calibrate == True):
            print ("Reading new Calibration\n")
            myfile = open('calibration.txt','r')
            i_offset = float(myfile.readline())
            j_offset = float(myfile.readline())
            y_offset = float(myfile.readline())
            myfile.close()
            calibrate = False
                    
    if request.method == 'POST':
        if request.form['submit']=='Off':
            m = 0
            u = 0
            lf = 0
            rf = 0
            lr = 0
            rr = 0
        elif request.form['submit']=='Front':
            m = 1
            u = 0
            lf = 0
            rf = 0
            lr = 0
            rr = 0
        elif request.form['submit']=='Passenger':
            m = 2
            u = 0
            lf = 0
            rf = 0
            lr = 0
            rr = 0
        elif request.form['submit']=='Driver':
            m = 3
            u = 0
            lf = 0
            rf = 0
            lr = 0
            rr = 0
        elif request.form['submit']=='Unhitch':
            if (m == 1):
                lf = 1
                rf = 1
                lr = 0
                rr = 0
                u = 0
                unhitch(m)
        elif request.form['submit']=='Hitch':
            if (m == 1):
                lf = 0
                rf = 0
                lr = 0
                rr = 0
                u = 0
                hitch(m)
        elif request.form['submit']=='Level':
            if (m > 0):
                lf = 0
                rf = 0
                lr = 0
                rr = 0
                u = 0
                level_jacks(m)                
                
        elif request.form['submit']=='Calibrate':
            u = 1
            print ('Calibrating Level')
            i_offset = i
            j_offset = j
            y_offset = y

                    
# Save Calibration to a file
            myfile = open('calibration.txt','w')
            myfile.write(str(i_offset)+'\n')
            myfile.write(str(j_offset)+'\n')
            myfile.write(str(y_offset)+'\n')
            myfile.close()
            calibrate = True

        elif request.form['submit']=='QUIT':
            shutdown = True
            time.sleep(1)
            os.system("sudo shutdown -h now")


    return render_template('index.html', i=i-i_offset, j=j-j_offset, lf=lf, rf=rf, lr=lr, rr=rr, m=m, a=a, u=u)

@app.route("/_level", methods=['GET'])
def level():
#    global i, j, y
    return jsonify(i=i, j=j)


getlevel = threading.Thread(target=get_level)

if __name__ == "__main__":
 
    if getlevel.is_alive() == False:
        getlevel.start() 
    app.run(host='0.0.0.0',port=5000, debug=True, use_reloader=False)
