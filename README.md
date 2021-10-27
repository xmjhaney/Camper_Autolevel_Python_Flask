# Python_Flask
This is code from a personal project - Python with Flask running on a Raspberry Pi

The following YouTube video demonstrates the working code:
Version 2 - shows current codebase in action

https://www.youtube.com/watch?v=aCiFrJ4rooo

Version 1 - initial concept

https://www.youtube.com/watch?v=vOFq5evArE0

For the code - 
level.py - contains all of the python code to run
          Uses rtimulib (you will need this library to run the python code)
          References ./templates/index.htmp (this contains the html/javascript for the user interface

unhitch.txt - contains the measurement when unhitched

calibrate.txt - contains the calibration measurement (level)

launcher.sh - launches level.py

RTIMULib.ini - initialization values for the inertial measuring unit that I used (populated with a utility included in the rtimulib package)

rtimulib - get information here
            https://github.com/RPi-Distro/RTIMULib
            https://github.com/RTIMULib/RTIMULib2
            

Hardware:
Raspberry Pi Zero W - 
            In order to run the Raspberry Pi zero W as a wireless AP, use the following (no need to enable routing)
            https://github.com/raspberrypi/documentation/blob/develop/documentation/asciidoc/computers/configuration/access-point-routed.adoc
            
            This runs on a standard version of Raspberry Pi OS
            
Inertial Measuring Unit - 
            Used an MPU-9250 System in Package (SiP) made by Spark Fun
            https://www.amazon.com/gp/product/B01JQ79FZS/ref=ppx_yo_dt_b_search_asin_title?ie=UTF8&psc=1
            https://www.microcenter.com/product/613058/IMU_Breakout_-_MPU-9250?storeID=125
            
Key-Fob and 12VDC relay board - 
            https://www.banggood.com/4CH-200M-Wireless-Remote-Control-Relay-Switch-Receiver-+-2-Transceiver-4-Channel-12V-DC-for-Smart-Home-p-1641748.html?cur_warehouse=CN&rmmds=search
            
5VDC Relay Board - 
            https://www.banggood.com/Geekcreit-5V-4-Channel-Relay-Module-For-PIC-ARM-DSP-AVR-MSP430-Geekcreit-for-Arduino-products-that-work-with-official-Arduino-boards-p-87987.html?cur_warehouse=CN&rmmds=search
            
TBD: Schematics for connecting the IMU to the RPI

TBD: Schematics for connecting the 5VDC relay board to the RPI

TBD: Directions for modifying the Keyfob to allow the 5VDC relay board to activate the remote buttons

TBD: Directions for connecting the 12VDC relay board into the existing camper landing gear controls/switches
            
