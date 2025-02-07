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
import supervisor
import sys

#Custom helper functions
from hh2025 import *

def hitblink():
    #Play hit animation
    hitblinktimer = 0.1
    pixels[0] = (128, 128, 0)

    motor.value = 1
    time.sleep(0.2)
    motor.value = 0

    led2.value = 0
    led3.value = 0
    led4.value = 0
    led5.value = 0

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

def game_over():
    while btn1.value == 0:
        pixels[0] = colors("red", basevalue=40)
        pixels[1] = colors("red", basevalue=40)
        pixels[2] = colors("red", basevalue=40)
        time.sleep(1)
        pixels[0] = colors("red", basevalue=128)
        pixels[1] = colors("red", basevalue=128)
        pixels[2] = colors("red", basevalue=128)
        time.sleep(0.1)
        pixels[0] = colors("red", basevalue=40)
        pixels[1] = colors("red", basevalue=40)
        pixels[2] = colors("red", basevalue=40)
        time.sleep(0.1)
        pixels[0] = colors("red", basevalue=128)
        pixels[1] = colors("red", basevalue=128)
        pixels[2] = colors("red", basevalue=128)
        time.sleep(0.1)

        pixels[0] = colors("red", basevalue=40)
        pixels[1] = colors("red", basevalue=40)
        pixels[2] = colors("red", basevalue=40)
    return 0

def reset_leds():
    led1.value = 0
    led2.value = 0
    led3.value = 0
    led4.value = 0
    led5.value = 0

def reset_pixels():
    pixels[0] = colors("off")
    pixels[1] = colors("off")
    pixels[2] = colors("off")

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
irin = pulseio.PulseIn(board.GP4, maxlen=100, idle_state=True)

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
batteryvoltage = get_voltage(sense) * 2

#Test code for LEDs
irled = digitalio.DigitalInOut(board.GP3)
irled.direction = digitalio.Direction.OUTPUT

led1.value = 1
led2.value = 1
led3.value = 1
led4.value = 1
led5.value = 1
irled.value = 1

pixels[0] = (16, 0, 0)
pixels[1] = (16, 0, 0)
pixels[2] = (16, 0, 0)

time.sleep(0.5)

pixels[0] = (0, 16, 0)
pixels[1] = (0, 16, 0)
pixels[2] = (0, 16, 0)

time.sleep(0.5)

pixels[0] = (0, 0, 16)
pixels[1] = (0, 0, 16)
pixels[2] = (0, 0, 16)

time.sleep(0.5)

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

team = 0
channel = 0
ledmode = 1
changingledmode = False
shots = 5
shotfired = False
hitcounter = 0

# Standard code comes with a default mode, a charging mode, an extra mode and
# an easter egg mode The function below switches to the next mode defined in
# variable `banane_modes` (below function).
def set_mode(init=0):
    if init == 1:
        return 0
    if current_mode < len(banana_modes) - 1:
        return current_mode + 1
    return 0

# Use banana_modes to define the modes you want to add. 0 is default, 1 is the
# charging mode, 2 is a predefined extra mode and 3 is an easter egg mode. To
# add new modes, simply add 4, 5, 6 etc. Don't skip any numbers in the
# sequence, the code will not work properly if you do.
# Please note that the `ledmode` is something different. It only controls the
# mode for the 5 orange indicator LEDs. It is available in the default (0)
# banana_mode and may be copied to other banana modes.
banana_modes = [0, 1, 2, 3]
current_mode = set_mode(init = 1)
mode_delay = 0.5

team_override = False

eggs = {
    0: "red",
    1: "green",
    2: "blue",
    3: "yellow",
    4: "magenta",
    5: "lightblue",
    6: "white", # cycle
    7: "orange",
    8: "lightgreen",
    9: "white", # rainbow
    10: "white", #colorswipe
    11: "white" #colorwave
}

def set_egg_mode(init=0, direction="forward"):
    if init == 1:
        return 0
    if direction == "forward":
        if current_egg < len(eggs) - 1:
            return current_egg + 1
        return 0
    if direction == "backward":
        if current_egg > 0:
            return current_egg - 1
        return 11
    return 0

current_egg = set_egg_mode(init=1)

while 1:
    # This should be the default mode.
    if current_mode == 0:
        #Team selection
        if team_override == False:
            if switch1.value == 1:
                pixels[1] = colors("red")
                team = 0
            else:
                pixels[1] = colors("green")
                team = 1
        else:
            if team == 2:
                pixels[1] = colors("blue")
            elif team == 3:
                pixels[1] = colors("yellow")
            elif team == 4:
                pixels[1] = colors("magenta")
            elif team == 5:
                pixels[1] = colors("lightblue")

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
                if team_override == False:
                    pulses = irmessage(team, 1, 0b0001, channel)
                else:
                    pulses = irmessage(team, 1, 8, channel)
                irin.pause()
                irled.send(barcolors[team])
                time.sleep(0.1)
                irled.send(pulses)
                irin.clear()
                irin.resume()
                pixels[0] = colors("blue")
                shots = shots - 1
            time.sleep(0.1)

        if swright.value == 1:
            shotfired = False

        n = supervisor.runtime.serial_bytes_available
        if n > 0:
            s = sys.stdin.read(1)
            pulses = irmessage((0b11100000 & ord(s)) >> 5, (0b00010000 & ord(s)) >> 4, 10, 0b00001111 & ord(s))
            irin.pause()
            irled.send(pulses)
            irin.clear()
            irin.resume()
            print(s, end="")

        if btn1.value == 1 and btn2.value == 1:
            # Request for data from badge, will display the data on serial
            # monitor. Such as serial number and battery data.
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
            ledmode -= 1
            if ledmode < 0:
                ledmode = 2

        #Button 2 test
        if btn2.value == 1 and changingledmode == False:
            changingledmode = True
            ledmode += 1
            if ledmode > 2:
                ledmode = 0

        if btn1.value == 0 and btn2.value == 0:
            changingledmode = False

        if ledmode == 0:
            pixels[0] = colors("red", 16)
            new_battery_voltage = get_voltage(sense) * 2
            batteryvoltage = batteryvoltage * 0.9 + new_battery_voltage * 0.1
            if batteryvoltage > 3.4:
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

            if batteryvoltage < 3.4:
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


        # Detecting IR signal
        if len(irin) > 34:
            # Put first pulse in a variable to be checked in while loop
            pulse = irin.popleft()
            if pulse > 7000 and pulse < 9000:
                # Keep looping until the trigger pulse of 8ms is detected
                pulses = []
                while len(irin) > 0:
                    # pop the space after the start pulse
                    pulse = irin.popleft()
                    if len(irin) > 32:
                        # Go through each of the 16 bits
                        for i in range(16):
                            #Pop the high pulse
                            pulse = irin.popleft()
                            # Capture the low pulse
                            pulse = irin.popleft()

                            # Convert to bits
                            if pulse < 1000:
                                pulses.append(0)
                            else:
                                pulses.append(1)

                irin.clear()
                if len(pulses) == 16:
                    recteam, rectrigger, reccommand, recparameter, crcvalid = decodeir(pulses)
                    if team != recteam and reccommand == 1:
                        print("Hit!")
                        hitblink()
                        hitcounter += 1
                    elif reccommand == 8:
                        team_override = True
                        team = recteam
                        hitblink()
                    elif reccommand == 10:
                        recbyte = (recteam << 5) + (rectrigger << 4) + recparameter
                        print(chr(recbyte), end="")

        if hitcounter > 4:
            print("Game over")
            hitcounter = game_over()

    elif current_mode == 1:
        # This is the charging mode. When charging, it will only turn on led5
        # and everything else is turned off. When not charging or done charging
        # one of the the neopixels (D1) will light up green.

        # Switch mode
        if swleft.value == 0:
            current_mode = set_mode()
            time.sleep(mode_delay)

        # Turn off pixel LEDs
        reset_pixels()

        # Initially turn off all indicator LEDs
        reset_leds()

        # new loop for charging and non charging mode. To avoid flickering of
        # the LEDs when initially turning it off repeatedly.
        while 1:
            # Switch mode (also breaks this inner loop)
            if swleft.value == 0:
                current_mode = set_mode()
                time.sleep(mode_delay)
                break
            # Charging mode (only led5 on)
            if chrg.value == 0:
                reset_pixels()
                led1.value = 0
                led2.value = 0
                led3.value = 0
                led4.value = 0
                led5.value = 1
            # Non charging mode (accu indicator)
            else:
                reset_leds()
                pixels[0] = colors("green", 5)

    elif current_mode == 2:
        # Here you can define your own banana mode. It is recommended to keep
        # at least the mode selection code, which is responding to the swleft
        # input. Otherwise you can't get back the other banana modes.

        pixels[1] = colors("magenta")
        pixels[2] = colors("magenta")

        # Mode selection
        if swleft.value == 0:
            current_mode = set_mode()
            time.sleep(mode_delay)

        # checks position of swtich1
        if switch1.value == 1:
            pass
        else:
            pass

        # checks position of switch2
        if switch2.value == 1:
            pass
        else:
            pass

        # if swleft if pressed (0 is pressed)
        if swleft.value == 0:
            pass

        # if swright if pressed (0 is pressed)
        if swright.value == 0:
            pass

        # if swmiddle if pressed (0 is pressed)
        if swmiddle.value == 0:
            pass

        # if btn1 is pressen (1 is pressed)
        if btn1.value == 1:
            pass

        # if btn2 is pressen (1 is pressed)
        if btn2.value == 1:
            pass

        # if btn1 and btn2 are pressen simultaneously
        if btn1.value == 1 and btn2.value == 1:
            pass


    elif current_mode == 3:
        # Easter Egg mode

        pixels[0] = colors(eggs[current_egg])
        pixels[1] = colors(eggs[current_egg])
        pixels[2] = colors(eggs[current_egg])

        # Mode selection
        if swleft.value == 0:
            current_mode = set_mode()
            time.sleep(mode_delay)

        if swright.value == 0 and shotfired == False:
            shotfired = True
            #generare pulse train and send them
            irin.pause()
            irled.send(barcolors[current_egg])
            time.sleep(0.1)
            irin.clear()
            irin.resume()
            time.sleep(0.1)

        if swright.value == 1:
            shotfired = False

        # if btn1 is pressen (1 is pressed)
        if btn1.value == 1:
            current_egg = set_egg_mode(direction="backward")
            time.sleep(0.5)

        # if btn2 is pressen (1 is pressed)
        if btn2.value == 1:
            current_egg = set_egg_mode(direction="forward")
            time.sleep(0.5)

    # elif current_mode == 2:
    #     # Uncomment this elif block if you want to add a third mode. Make sure
    #     # you also add a new mode to the banana_modes list. So in this case the
    #     # banana_modes should be [0, 1, 2]. Repeat this for any extra mode you
    #     # want to add to the code.

    #     pixels[1] = colors("blue")
    #     pixels[2] = colors("blue")

    #     # Mode selection
    #     if swleft.value == 0:
    #         current_mode = set_mode()
    #         time.sleep(mode_delay)
