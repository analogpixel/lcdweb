#!/usr/bin/python

import RPi.GPIO as GPIO
import time
from flask import Flask

clk=24
cs=25
din=8

GPIO.setmode(GPIO.BCM)
GPIO.setup(clk, GPIO.OUT)
GPIO.setup(cs, GPIO.OUT)
GPIO.setup(din, GPIO.OUT)

def writeByte(addr,byte):
  # start the seq. with cs low
  GPIO.output(cs,0)

  # start from the left and send 1 bit at a time
  # clock low, send bit, clock high
  for i in range(8,0,-1):
    GPIO.output ( clk, 0)
    GPIO.output ( din, (2**(i-1) & addr) >> (i-1) )
    GPIO.output ( clk, 1)

  for i in range(8,0,-1):
    GPIO.output ( clk, 0)
    GPIO.output ( din, (2**(i-1) & byte) >> (i-1) )
    GPIO.output ( clk, 1)

  # end the seq. with cs high
  GPIO.output(cs,1)

# init
writeByte(0x09, 0x00) # set decode mode
writeByte(0x0a, 0x01) # set the intensity
writeByte(0x0b, 0x07) # scan limit
writeByte(0x0f, 0x00) # switch from display test mode to normal op.


app = Flask("lcd")

@app.route("/")
def index():
  return render_template('index.html')

@app.route("/set/<addr>/<byte>")
def setByte(addr, byte):
  writeByte(int(addr), int(byte))
  return "ok"

if __name__ == "__main__":
  app.run(host='0.0.0.0',debug=True)

# 4 trash bits then 4bit addr then 8bit data
# writeByte(1, 0b00111100) #00111100
# writeByte(2, 0x42) #01000010
# writeByte(3, 0x42)
# writeByte(4, 0x42)
# writeByte(5, 0x3c)
# writeByte(6, 0x42)
# writeByte(7, 0x42)
# writeByte(8, 0x3c)

# for x in range(8):
#   for y in range(8):
#     if x ==y:
#       writeByte(y+1, 0xff)
#     else:
#       writeByte(y+1, 0x00)

#   time.sleep(.2)

GPIO.cleanup()
