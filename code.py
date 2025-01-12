#General imports
import board
import digitalio
import time

#imports for the IR receiver
import pulseio
import array

#Neopixel initialisation
import neopixel
pixels = neopixel.NeoPixel(board.GP2, 3)

#Import for battery voltage
from analogio import AnalogIn

#Import support for reading out serial number and other data
import microcontroller

#Custom helper functions
from hh2025 import *

def hitblink():
    #Play hit animation
    hitblinktimer = 0.2
    pixels[0] = (128, 128, 0)

    motor.value = 1
    time.sleep(0.2)
    motor.value = 0

    led1.value = 1
    time.sleep(hitblinktimer)
    led2.value = 1
    time.sleep(hitblinktimer)
    led3.value = 1
    time.sleep(hitblinktimer)
    led4.value = 1
    time.sleep(hitblinktimer)
    led5.value = 1
    time.sleep(hitblinktimer)

    

    led1.value = 0
    time.sleep(hitblinktimer)
    led2.value = 0
    time.sleep(hitblinktimer)
    led3.value = 0
    time.sleep(hitblinktimer)
    led4.value = 0
    time.sleep(hitblinktimer)
    led5.value = 0
    time.sleep(hitblinktimer)

    

    pixels[0] = (0, 0, 0)


#Init top selection switches
switch1 = digitalio.DigitalInOut(board.GP0)
switch1.direction = digitalio.Direction.INPUT
switch2 = digitalio.DigitalInOut(board.GP1)
switch2.direction = digitalio.Direction.INPUT

#Init for bottom buttons and LEDs
btn1 = digitalio.DigitalInOut(board.GP5)
btn1.direction = digitalio.Direction.INPUT
led1 = digitalio.DigitalInOut(board.GP6)
led1.direction = digitalio.Direction.OUTPUT
led2 = digitalio.DigitalInOut(board.GP7)
led2.direction = digitalio.Direction.OUTPUT
led3 = digitalio.DigitalInOut(board.GP8)
led3.direction = digitalio.Direction.OUTPUT
led4 = digitalio.DigitalInOut(board.GP9)
led4.direction = digitalio.Direction.OUTPUT
led5 = digitalio.DigitalInOut(board.GP10)
led5.direction = digitalio.Direction.OUTPUT
btn2 = digitalio.DigitalInOut(board.GP11)
btn2.direction = digitalio.Direction.INPUT

#init for IR LED and receiver. Commented out here for testcode below
#irled = pulseio.PulseOut(board.GP3, frequency=38000, duty_cycle=32768)
#pulses = array.array('H',(65000,1000,65000,1000))
irin = pulseio.PulseIn(board.GP4, maxlen=40, idle_state=True)

#Init for trigger switch
swleft = digitalio.DigitalInOut(board.GP16)
swleft.direction = digitalio.Direction.INPUT
swmiddle = digitalio.DigitalInOut(board.GP17)
swmiddle.direction = digitalio.Direction.INPUT
swright = digitalio.DigitalInOut(board.GP18)
swright.direction = digitalio.Direction.INPUT

#Init for optional motor
motor = digitalio.DigitalInOut(board.GP19)
motor.direction = digitalio.Direction.OUTPUT

#Init for SAO connector
saosda = board.GP20
saoscl = board.GP21
saogp1 = digitalio.DigitalInOut(board.GP22)
saogp1.direction = digitalio.Direction.OUTPUT
saogp2 = digitalio.DigitalInOut(board.GP23)
saogp2.direction = digitalio.Direction.OUTPUT

#Init for battery management
chrg = digitalio.DigitalInOut(board.GP25)
chrg.direction = digitalio.Direction.INPUT
sense = AnalogIn(board.A0)

#Test code for LEDs
irled = digitalio.DigitalInOut(board.GP3)
irled.direction = digitalio.Direction.OUTPUT

pixels[0] = (16, 16, 16)
pixels[1] = (16, 16, 16)
pixels[2] = (16, 16, 16)

led1.value = 1
led2.value = 1
led3.value = 1
led4.value = 1
led5.value = 1
irled.value = 1

time.sleep(0.7)

pixels[0] = (0, 0, 0)
pixels[1] = (0, 0, 0)
pixels[2] = (0, 0, 0)

led1.value = 0
led2.value = 0
led3.value = 0
led4.value = 0
led5.value = 0
irled.value = 0

irled.deinit()

#Init for main code
irled = pulseio.PulseOut(board.GP3, frequency=38000, duty_cycle=32768)
#pulses = array.array('H',(65000,1000,65000,1000))

team = 0
channel = 0
ledmode = 1
changingledmode = False
shots = 5
shotfired = False
hitcounter = 0

def set_mode(init=0):
    if init == 1:
        return 0
    if current_mode < len(modes) - 1:
        return current_mode + 1
    return 0

modes = [0, 1]
current_mode = set_mode(init = 1)
mode_delay = 0.5

while 1:
    # This should be the default mode.
    if current_mode == 0:
        #Team selection
        if switch1.value == 1:
            pixels[1] = colors("red")
            team = 0
        else:
            pixels[1] = colors("green")
            team = 1

        #Channel selection
        if switch2.value == 1:
            pixels[2] = colors("magenta")
            channel = 0
        else:
            pixels[2] = colors("yellow")
            channel = 1

        # Mode selection
        if swleft.value == 0:
            current_mode = set_mode()
            time.sleep(mode_delay)

        #Trigger middle
        if swmiddle.value == 0:
            pixels[0] = (0, 64, 0)
            shots = 5

        #Trigger pull
        if swright.value == 0 and shotfired == False:
            shotfired = True
            if shots > 0:
            #generare pulse train and send them
                pulses = irmessage(team, 1, 0b0001, channel)
                irled.send(barcolors[team])
                time.sleep(0.1)
                irled.send(pulses)
                pixels[0] = colors("blue")
                shots = shots - 1
            time.sleep(0.1)

        if swright.value == 1:
            shotfired = False

        if btn1.value == 1 and btn2.value == 1:
            #request for data from badge
            #Get serial number
            uid = microcontroller.cpu.uid
            for bt in uid:
                print(f"{bt:X}",end="")
            print()
            #Battery data
            print(f"Charging = {chrg.value}")
            print(f"Battery voltage = {get_voltage(sense)*2}V")
            time.sleep(1)

        if btn1.value == 1 and changingledmode == False:
            changingledmode = True
            ledmode = ledmode - 1
            if ledmode < 0:
                ledmode = 2

        #Button 2 test
        if btn2.value == 1 and changingledmode == False:
            changingledmode = True
            ledmode +=1
            if ledmode > 2:
                ledmode = 0

        if btn1.value == 0 and btn2.value == 0:
            changingledmode = False

        if ledmode == 0:
            pixels[0] = colors("red", 16)
            batteryvoltage = get_voltage(sense) * 2
            if batteryvoltage > 3.3:
                led1.value = 1
            else:
                led1.value = 0
            
            if batteryvoltage > 3.6:
                led2.value = 1
            else:
                led2.value = 0

            if batteryvoltage > 3.8:
                led3.value = 1
            else:
                led3.value = 0

            if batteryvoltage > 4.0:
                led4.value = 1
            else:
                led4.value = 0

            if chrg.value == 1:
                led5.value = 0
            else:
                led5.value = 1

            if batteryvoltage < 3.3:
                pixels[0] = (1, 0, 0)
                pixels[1] = (1, 0, 0)
                pixels[2] = (1, 0, 0)

        elif ledmode == 1:
            if shots > 0:
                pixels[0] = colors("green", 16)
                led1.value = 1
            else:
                pixels[0] = colors("red", 128)
                led1.value = 0

            if shots > 1:
                led2.value = 1
            else:
                led2.value = 0

            if shots > 2:
                led3.value = 1
            else:
                led3.value = 0

            if shots > 3:
                led4.value = 1
            else:
                led4.value = 0

            if shots > 4:
                led5.value = 1
            else:
                led5.value = 0

        elif ledmode == 2:
            if hitcounter > 0:
                led1.value = 1
            else:
                led1.value = 0

            if hitcounter > 1:
                led2.value = 1
            else:
                led2.value = 0

            if hitcounter > 2:
                led3.value = 1
            else:
                led3.value = 0

            if hitcounter > 3:
                led4.value = 1
            else:
                led4.value = 0

            if hitcounter > 4:
                pixels[0] = colors("red", 128)
                led5.value = 1
            else:
                pixels[0] = colors("blue", 16)
                led5.value = 0



        #Detecting IR signal
        if len(irin) > 34:
            print("---          start            ---")
            #Put first pulse in a variable to be checked in while loop
            pulse = irin.popleft()
            pulses = []
            while len(irin) > 0:
                #Keep looping until the trigger pulse of 8ms is detected
                if pulse > 7000 and pulse < 9000:
                    print("Startpulse found")
                    #pop the space after the start pulse
                    pulse = irin.popleft()
                    print(len(irin))
                    #check if the start pulse was found at the beginning of the capture
                    if len(irin) == 33:
                        print("Correct amount of pulses found")
                        #Go through each of the 16 bits
                        for i in range(16):
                            #Pop the high pulse
                            pulse = irin.popleft()
                            #Capture the low pulse
                            pulse = irin.popleft()

                            #Convert to bits
                            if pulse < 1000:
                                pulses.append(0)
                            else:
                                pulses.append(1)

                            print(pulse)
                else:
                    #keep searching for the start
                    pulse = irin.popleft()
                    print(pulse)
            
            irin.clear()
            print(pulses)
            if len(pulses) == 16:
                print(checkcrc(pulses))
                recteam, rectrigger, reccommand, recparameter, crcvalid = decodeir(pulses)
                print(f"Team: {recteam}, Command: {reccommand}, Parameter: {recparameter}")
                if team != recteam and reccommand == 1:
                    print("Hit!")
                    hitblink()
                    hitcounter += 1
    
    elif current_mode == 1:
        # Mode selection
        print('Alt mode')

        pixels[1] = colors("magenta")
        pixels[2] = colors("magenta")

        # Mode selection
        if swleft.value == 0:
            current_mode = set_mode()
            time.sleep(mode_delay)
