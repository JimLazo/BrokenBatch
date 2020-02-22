from tkinter import * 
from gpiozero import PWMOutputDevice, LED, Button as GP
import csv
# Needs to be imported as "hx" to work later on
import HX711 as hx #pin 38 is the data pin, pin 40 is the sclk.
class Window(Frame):
    #initializes parameters
    def __init__(self, master=None):
        Frame.__init__(self, master)                 
        self.master = master
        self.init_window()
        self.init_GPIO()
        
        
        #creates the window widget
    def init_window(self, bg= "Black"):
        self.configure(background=bg)
        self.master.title("GUItest") #parent widget
        self.pack(fill=BOTH, expand = 1) #give parent widget the whole window
        #Parameters
        self.CValue = 0
        self.CName = "PSBC"
        self.MaxCValue = 0
        self.TMaxValue = 0
        self.MaxTeamName = 'none yet'
        #Images
        bgImg = Image.open("Background.jpg")
        render = ImageTk.PhotoImage(bgImg)
        img = Label(self, image=render)
        img.image = render
        img.place(x=0, y=0, relwidth=1, relheight=1)
        #Labels
        #separated for my own clarity, these are used to load and update the text
        self.textWeight= Label(self, bg= None, fg= 'Black', text ="Weight Bared = " +str(self.CValue), font = ('Arial', 80), height = 2, relief = RIDGE )
        self.textWeight.pack(side = RIGHT)
        self.tName= Label(self,bg= None, fg= 'Black', text = self.CName, font = ('Arial', 80), height = 2, relief = RIDGE )
        self.tName.pack(side = TOP)
    

        #Buttons
        ForwardButton= Button(text= 'Forward', command = self.Forward)  #create test button, remove and replace with GPIO button
        ForwardButton.pack(side=BOTTOM)
        BackButton= Button(text='Backward', command= self.Backward) #create test button, remove and replace with GPIO button
        BackButton.pack(side=BOTTOM)
        test3= Button(text='Brake', command= self.Brake) #create test button, remove and replace with GPIO button
        test3.pack(side=BOTTOM)

    def init_GPIO(self):
        #The pins that will control the Hbridge are pins 11,12,13,14. 
        #pin 12 is meant for PWM.
        self.pin22 = PWMOutputDevice(25)
        self.pin22.frequency = 1000
        self.pin22.value= 0.00
        #Pins 11 and 13 are meant for motion. 11 goes to to topmost IO on the driver. 11 is IN 1
        self.pin16 = LED(23)
        self.pin14 = LED(24)
        #pin15 is meant for the button to start. The other end connects to 3v3 at pin 17.
        self.start= GP.Button(22)
        self.start.pull_up = False #Active Low button, write true for Active High
        self.start.bounce_time = 0.5  #prevents double clicking really fast
        self.start.when_pressed = StartRead #Bad programming, i couldnt figure it out any other way : (
    


#From here on, this concerns Driver Controls.
        #Call to Move Motor Forward
    def Forward(self):
        self.pin22.value = 0.25
        self.pin18.off()
        self.pin16.on()

          #Call to Move Motor Backward      
    def Backward(self):
        self.pin22.value = 0.25
        self.pin16.off()
        self.pin18.on()

        #Call for Fullspeed Forward
    def FullForward(self):
        Forward()
        self.pin22.value=1

        #Call for Fullspeed Backward
    def FullBackward(self):
        Backward()
        self.pin22.value =1

        #Call for Brake
    def Brake(self):
        self.pin16.off()
        self.pin18.off()
        self.pin22.value= 0

        #Call for Neutral State
    def Neutral(self):
        self.pin22.value = 0
        self.pin16.on()
        self.pin18.on()
#From Here on, this is the stuff that concerns the buttons.
#The bad programming starts here.
    def StartRead(self):
        self.start = None #Turn off the start button.
        ReadOp() # Not sure what this is, will investigate -Jim
                
    def TurnoffAll(self):
        self.destroy()

#From here on this is the stuff that concerns the HX711/Load Cell
    def GetValue(self):
        self.CValue = hx.getValue() #the Value straight from the ADC

    def tare(self):
        hx.tare() #It does what it says -_-


#From here on this is the stuff that concerns the Digital Potentiometer

#From here on this is the stuff that concerns running the GUI
    
    #writes data as a CSV
    def WriteCSV(self):
        with open('BridgeData.csv', 'a') as csvfile: #this is to creat/open a file, the a is to write at the end of the file.
            filewrite= csv.writer(csvfile)
            filewrite.writerow([self.c1, self.c2, self.c3])  #these are placeholders for actual variables.
            iteration = iteration + 1
     
                        #this is for reading the team name and weight of the bridge in 1st place.
    def ReadCSVMax(self):
        loopIter = -1
        with open('BridgeData.csv', 'r') as csvfile:
             read= list(csv.reader(csvfile, delimiter= ','))#fucking shit, im stuck here.
             for row in read:            
                if row:
                    self.names.append(row[0])
                    self.weights.append(row[1])
             for number in self.weights:
                loopIter += 1
                if number:
                    if loopIter == 0:
                        continue
                    if loopIter == 1:
                        self.tMaxwght= float(self.weights[loopIter])
                        self.tMaxName= self.names[loopIter]
                    else:
                         if self.tMaxwght < float(self.weights[loopIter]):
                            self.tMaxwght =float(self.weights[loopIter])   
     

root = Tk() 
root.attributes('-fullscreen', True)
app = Window(root) # creates the instance 
#this is the equivalent to while(1). 
root.mainloop()
