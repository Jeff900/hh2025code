# Pim's Banana
The badge comes with a default bananamode and an option to create new bananamodes. The following documentation will focus on the default mode. If you want to read about creating your own mode, read the 'Alternative modes' section.

## Default mode
switch1
switch2
btn1
btn2
s1

irin
irled

## Alternative modes
One of the ideas with this badge is that as much people as possible should be able to play with the code. That's why it is written in CircuitPython. You can alter to code and upload it and that is bassically it. But if you want to keep the original code and want build on top of it, there is some structure available to do so. You can read that here.

(Btw, you don't have to stick with the default code or even CircuitPython!)

### Using the alternative mode
Next to the default mode there is one alternative mode already embedded in the main loop. Every time the loop executes it will check the `current_mode`. By default the current mode is 0 and this is by default the only banana mode available/configured. To add a banana mode, you should edit the `banana_modes` variable. This is by default this list `[0]`, it only contains the default mode 0. Change it to `[0, 1]`, to make the alternative mode available. 

Since the code for this banana mode was already embedded it will work immediately, although the only working feature is to set the next mode (because otherwise you're not able the change the mode as soon as you). Also we set up some of the basic interactions/triggers you could now code yourself.