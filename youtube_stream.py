#!/usr/bin/env python3
import subprocess
import picamera
import time
import os
import configparser

config = configparser.ConfigParser()
config.read('/home/pi/birdcam/apikey.ini')
os.environ['TZ'] = 'Europe/Berlin'
time.tzset()

YOUTUBE="rtmp://a.rtmp.youtube.com/live2/"
KEY=config["Youtube"]["key"]
stream_cmd = 'ffmpeg -f h264 -r 25 -i - -itsoffset 5.5 -fflags nobuffer -f alsa -i hw:1,0 -vcodec copy -acodec aac -ac 1 -ar 8000 -ab 32k -map 0:0 -map 1:0 -strict experimental -f flv ' + YOUTUBE + KEY
stream = subprocess.Popen(stream_cmd, shell=True, stdin=subprocess.PIPE)
camera = picamera.PiCamera(resolution=(1296, 730), framerate=25)
try:
  now = time.strftime("%Y-%m-%d-%H:%M:%S")
  camera.framerate = 25
  camera.vflip = True
  camera.hflip = True
  camera.color_effects = (128,128)
  camera.contrast = 35
  camera.drc_strength = "medium"
  camera.sharpness = 35
  camera.video_denoise = False
  camera.start_recording(stream.stdin, format='h264', bitrate = 2000000)
  while True:
     camera.wait_recording(1)
     now = time.strftime("%Y-%m-%d-%H:%M:%S")
     camera.annotate_text = now
except KeyboardInterrupt:
     camera.stop_recording()
finally:
  camera.close()
  stream.stdin.close()
  stream.wait()
  print("Camera safely shut down")
  print("Good bye")

