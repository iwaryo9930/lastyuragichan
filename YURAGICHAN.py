import paho.mqtt.client as mqtt
import os
import urllib.parse as urlparse
import RPi.GPIO as GPIO
import time                         #時間制御用のモジュールをインポート
import sys                          #sysモジュールをインポート
import random
import threading


# Define event callbacks
def on_connect(client, userdata, flags, rc):
    print("rc: " + str(rc))

def on_message(client, obj, msg):
    global changecode
    
    if msg.payload == b'1':
        changecode = 1   
    elif msg.payload == b'2':
        changecode = 2
    elif msg.payload == b'3':
        changecode = 3
    elif msg.payload == b'0':
        changecode = 0
  
        
def on_subscribe(client, obj, mid, granted_qos):
    print("Subscribed: " + str(mid) + " " + str(granted_qos))

def on_log(client, obj, level, string):
    print(string)
    
def loopstart():
    # Continue the network loop, exit when an error occurs
    rc = 0
    while rc == 0:
        rc = mqttc.loop_start()
    print("rc: " + str(rc))
    
def lightning():
    #while文で無限ループ
    #LEDの明るさをデューティ比で制御
    #Led.ChangeDutyCycle(デューティ比)
    global changecode
    changecode = 0
    Led_pin = 25     #変数"Led_pin"に25を代入
    #PWMの設定
    Led = GPIO.PWM(Led_pin, 50)   #GPIO.PWM(ポート番号, 周波数[Hz])
    #初期化処理
    Led.start(0)                  #PWM信号0%出力
    GPIO.output(Led_pin,GPIO.HIGH)
    
    while True:
        try:
            if changecode == 1:
                x = random.random()
                bright = 100*x
                Led.ChangeDutyCycle(bright)    #PWM信号出力(デューティ比は変数"bright")
                time.sleep(0.07)               #0.05秒間待つ
            elif changecode == 2:
                x = random.random()
                bright = 100*x
                Led.ChangeDutyCycle(bright)    #PWM信号出力(デューティ比は変数"bright")
                time.sleep(0.5)                #0.5秒間待つ
            elif changecode == 3:
                x = random.random()
                bright = 100*x
                Led.ChangeDutyCycle(bright)    #PWM信号出力(デューティ比は変数"bright")
                time.sleep(1)                  #0.1秒間待つ
            elif changecode == 0:
                Led.ChangeDutyCycle(0)         #PWM信号出力(デューティ比は変数"bright")
                GPIO.output(Led_pin,GPIO.LOW)
                
                
                
        except KeyboardInterrupt:              #Ctrl+Cキーが押された
                Led.stop()                     #LED点灯をストップ
                GPIO.cleanup()                 #GPIOをクリーンアップ
                sys.exit()                     #プログラムを終了
            

       

#threading 
thread_001 = threading.Thread(target=loopstart)
thread_002 = threading.Thread(target=lightning)

#GPIO setup
GPIO.setmode(GPIO.BCM)
GPIO.setup(25 , GPIO.OUT)

#global variable to change lightning mode
global changecode

# MQTT setup 
mqttc = mqtt.Client()
# Assign event callbacks
mqttc.on_message = on_message
mqttc.on_connect = on_connect
mqttc.on_subscribe = on_subscribe

# Uncomment to enable debug messages
#mqttc.on_log = on_log

# Parse CLOUDMQTT_URL (or fallback to localhost)
url_str = os.environ.get('driver.cloudmqtt.com', 'mqtt://localhost:1883')
url = urlparse.urlparse(url_str)
topic = url.path[1:] or ''

# Connect　※
mqttc.username_pw_set('','')
mqttc.connect('',)

# Start subscribe, with QoS level 0
mqttc.subscribe(topic, 0)

#  thread start
thread_001.start()
thread_002.start()
