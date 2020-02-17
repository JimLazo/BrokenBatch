import gpiozero as gpio
import time
import numpy

HIGH=1
LOW=0
class HX711:
  def __init__(self, gain=128):
    #set data and clock pins (BCM)
    self.DT =20
    self.SCK=21

    

    self.sample=0
    self.val=0
    
    
    self.GAIN = 0
    self.OFFSET = 0
    self.SCALE = 1
    self.lastVal = 0

    gpio.setwarnings(False)
    gpio.setmode(gpio.BCM)
    gpio.setup(self.SCK, gpio.OUT)
    
  def setCursor(x,y):
      if y == 0:
          n=128+x
      elif y == 1:
          n=192+x
      lcdcmd(n)

  def getValue(self):
    i=0
    Count=0
    gpio.setup(self.DT, gpio.OUT)
    gpio.output(self.DT,1)
    gpio.output(self.SCK,0)
    gpio.setup(self.DT, gpio.IN)

    while gpio.input(self.DT) == 1:
        i=0
    for i in range(24):
          gpio.output(self.SCK,1)
          Count=Count<<1

          gpio.output(self.SCK,0)
          #time.sleep(0.001)
          if gpio.input(self.DT) == 0: 
              Count=Count+1
              #print Count
          
    gpio.output(self.SCK,1)
    Count=Count^0x800000
    #time.sleep(0.001)
    gpio.output(self.SCK,0)
    return Count  

  #begin()

  def read_average(self, times=3):
      total = 0
      for i in range(times):
          total += self.getValue()

      return total / times

  def get_value(self, times=3):
      return self.read_average(times) - self.OFFSET

  def get_units(self, times=3):
      return self.get_value(times) / self.SCALE

  def tare(self, times=15):
      total = self.read_average(times)
      print("sum", total)
      self.set_offset(total)

  def SetScale(self, scale):
      self.SC
      ALE = scale

  def set_offset(self, offset):
      self.OFFSET = offset
  #time.sleep(3)
  #sample = getValue()
  #flag=0
  #highest = 0
  #while 1:
      #count= getValue()
      #w=0
      #w=(sample-count)*(0.0022) *(.035528) #(sample-count) (grams to pounds)(Scale factor Per LoadCell)
      #w= numpy.absolute(w)
      #time.sleep(.3)
  #    print '%.2f' % w,"lbs"
     

