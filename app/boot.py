import esp32
import os
import time
from time import sleep
import dht
import machine
import network

try:
  import usocket as socket
except:
  import socket
 
led = machine.Pin(2, machine.Pin.OUT)
token='b8639604e11075dce65f6a89a2a04754aa1c18bb'
def callback(p):
 print('pin change', p)
 
p13 = machine.Pin(13, machine.Pin.IN)
p13.irq(trigger=machine.Pin.IRQ_FALLING, handler=callback)
print(p13.value())

  
T_COLOR = '#f5b041'
H_COLOR = '#85c1e9'
ERR_COLOR = '#444444'

T_VPIN = 3
H_VPIN = 4

dht22 = dht.DHT22(machine.Pin(4, machine.Pin.IN, machine.Pin.PULL_UP))




def do_connect():
 print("conect") 
 sta_if = network.WLAN(network.STA_IF)
 if not sta_if.isconnected():
        print('connecting to network...')
        sta_if.active(True)
        sta_if.connect(ssid, password)
        while not sta_if.isconnected():
            pass
 print('network config:', sta_if.ifconfig())

if machine.reset_cause() == machine.DEEPSLEEP_RESET:
    print('woke from a deep sleep')
    
    f=open('wifi.dat')
    wifidat=f.read()
    ssid, password, api = wifidat.strip("\n").split(";")
    print(api)
    print("Connecting to Blynk server...",api)
    do_connect()
    import app.blynk_mp as blynklib
    try:
     blynk = blynklib.Blynk(api)
# return  wlan_sta if connected else None
    except:

     print("BAD BLYNK:")
else:
    print('power on or hard reset')
    import app.wifimgr as wifimgr
    wlan = wifimgr.get_connection()
    if wlan is None:
         print("Could not initialize the network connection.")
         while True:
             pass
              #pass  # you shall not pass <img draggable="false" role="img" class="emoji" alt="😀" src="https://s0.wp.com/wp-content/mu-plugins/wpcom-smileys/twemoji/2/svg/1f600.svg" scale="0">
              # Main Code goes here, wlan is a working network.WLAN(STA_IF) instance.
    print("ESP OK")
    import ntptime
    print("Local time before synchronization：%s" %str(time.localtime()))
    ntptime.settime()
    print("Local time after synchronization：%s" %str(time.localtime()))

    import app.blynk_mp as blynklib
    f=open('wifi.dat')
    wifidat=f.read()
    ssid, password, api = wifidat.strip("\n").split(";")
    print(api)
    print("Connecting to Blynk server...",api)
    try:
      blynk = blynklib.Blynk(api)
     # return  wlan_sta if connected else None
    except:
       print("BAD BLYNK:")

def ota():
 from app.ota_updater import OTAUpdater
#def download_and_install_update_if_available():
     # o = OTAUpdater('https://github.com/sensorwifi/ota_door')
     #otaUpdater = OTAUpdater('https://github.com/rdehuyss/chicken-shed-mgr', github_src_dir='app', main_dir='app', secrets_file="secrets.py")
 o = OTAUpdater('https://github.com/sensorwifi/ota_door_temperature', main_dir='app', headers={'Authorization': 'token {}'.format(token)})
 print(o)
 o.install_update_if_available_after_boot(ssid, password)
 print(update)

 
def hall_100(hall):
  print("Alert 100 - default - reset wifi and blynk")
  machine.reset()
    #os.remove("wifi.dat")
    

def hall_10():
  print("Alert 10  - reset ")
 # machine.deepsleep(10000)
  print("OTA-------------------")
  ota()
  #o = OTAUpdater('https://github.com/sensorwifi/ota_door', github_src_dir='app', main_dir='app')
 # o._get.
  #o.install_update_if_available_after_boot()
  
  #download_and_install_update_if_available()

def read_handler(vpin):
    temperature = 0.0
    humidity = 0.0

    # read sensor data
    try:
        dht22.measure()
        temperature = dht22.temperature()
        humidity = dht22.humidity()
    except OSError as o_err:
        print("Unable to get DHT22 sensor data: '{}'".format(o_err))

    # change widget values and colors according read results
    if temperature != 0.0 and humidity != 0.0:
        blynk.set_property(T_VPIN, 'color', T_COLOR)
        blynk.set_property(H_VPIN, 'color', H_COLOR)
        blynk.virtual_write(T_VPIN, temperature)
        blynk.virtual_write(H_VPIN, humidity)
    else:
        # show widgets aka 'disabled' that mean we had errors during read sensor operation
        blynk.set_property(T_VPIN, 'color', ERR_COLOR)
        blynk.set_property(H_VPIN, 'color', ERR_COLOR)

       
def conect_blynk():
  
  x = 0
  blynk.run()
  print("to blynk")
  while x < 3:
    read_handler(4)
    time.sleep_ms(180)
    print(x)
    x+=1


  
while True:
 #print(p13)
 if p13.value()==1:
  alarm=True
 else:
  alarm=False 
 
 hall = esp32.hall_sensor()
 if hall > 100 : hall_100(hall)
 if hall < 10 : hall_10()
 time.sleep_ms(180)
 conect_blynk()
 print("I go slepp")
 reed = machine.Pin(13, mode = machine.Pin.IN, pull = machine.Pin.PULL_DOWN)
 reed.irq(trigger=machine.Pin.WAKE_LOW, wake=machine.DEEPSLEEP)
 print(alarm)
 if alarm is True: 
  machine.deepsleep(30000)
 else:
  pass
  
 

