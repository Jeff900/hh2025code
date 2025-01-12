import array

def irmessage(team=0, trigger=1, command=1, parameter=0):
    bits = [0]*16

    bits[0] = team & 0b1
    bits[1] = (team >> 1) & 0b1
    bits[2] = (team >> 2) & 0b1

    bits[3] = trigger

    bits[4] = command & 0b1
    bits[5] = (command >> 1) & 0b1
    bits[6] = (command >> 2) & 0b1
    bits[7] = (command >> 3) & 0b1

    bits[8] = parameter & 0b1
    bits[9] = (parameter >> 1) & 0b1
    bits[10] = (parameter >> 2) & 0b1
    bits[11] = (parameter >> 3) & 0b1

    bits[12] = bits[11] ^ bits[10] ^ bits[9] ^ bits[8] ^ bits[6] ^ bits[4] ^ bits[3] ^ bits[0]
    bits[13] = bits[8] ^ bits[7] ^ bits[6] ^ bits[5] ^ bits[3] ^ bits[1] ^ bits[0] ^ 1
    bits[14] = bits[9] ^ bits[8] ^ bits[7] ^ bits[6] ^ bits[4] ^ bits[2] ^ bits[1] ^ 1
    bits[15] = bits[10] ^ bits[9] ^ bits[8] ^ bits[7] ^ bits[5] ^ bits[3] ^ bits[2]

    pulses = array.array('H',(8400, 4200))

    for bit in bits:
        pulses.append(526)
        if bit == 1:
            pulses.append(1574)
        else:
            pulses.append(526)
    
    pulses.append(526)
    pulses.append(40000)

    return pulses

def checkcrc(bits):
    bit1 = bits[11] ^ bits[10] ^ bits[9] ^ bits[8] ^ bits[6] ^ bits[4] ^ bits[3] ^ bits[0]
    bit2 = bits[8] ^ bits[7] ^ bits[6] ^ bits[5] ^ bits[3] ^ bits[1] ^ bits[0] ^ 1
    bit3 = bits[9] ^ bits[8] ^ bits[7] ^ bits[6] ^ bits[4] ^ bits[2] ^ bits[1] ^ 1
    bit4 = bits[10] ^ bits[9] ^ bits[8] ^ bits[7] ^ bits[5] ^ bits[3] ^ bits[2]

    if bit1 == bits[12] and bit2 == bits[13] and bit3 == bits[14] and bit4 == bits[15]:
        return True
    else:
        return False

def decodeir(bits):
    team = bits[0]
    team = team + (bits[1] << 1)
    team = team + (bits[2] << 2)

    trigger = bits[3]

    command = bits[4]
    command = command + (bits[5] << 1)
    command = command + (bits[6] << 2)
    command = command + (bits[7] << 3)

    parameter = bits[8]
    parameter = parameter + (bits[9] << 1)
    parameter = parameter + (bits[10] << 2)
    parameter = parameter + (bits[11] << 3)

    crcvalid = checkcrc(bits)

    return [team, trigger, command, parameter, crcvalid]

def colors(color, basevalue = 40):
    basevalue_half = basevalue / 2
    if  color == 'red':
        return (basevalue, 0, 0)
    elif color == 'orange':
        return (basevalue, basevalue_half, 0)
    elif color == 'yellow':
        return (basevalue, basevalue, 0)
    elif color == 'lightgreen':
        return (basevalue_half, basevalue, 0)
    elif color == 'green':
        return (0, basevalue, 0)
    elif color == 'springgreen':
        return (0, basevalue, basevalue_half)
    elif color in ['cyan', 'lightblue']:
        return (0, basevalue, basevalue)
    elif color == 'azure':
        return (0, basevalue_half, basevalue)
    elif color == 'blue':
        return (0, 0, basevalue)
    elif color == 'violet':
        return (basevalue_half, 0, basevalue)
    elif color == 'magenta':
        return (basevalue,0,basevalue)
    elif color == 'rose':
        return (basevalue, 0, basevalue_half)
    elif color == 'white':
        return (basevalue, basevalue, basevalue)
    else:
        return (0, 0, 0)

barred = array.array('H',(9071,4523,571,566,571,566,571,566,571,566,571,565,571,566,571,566,571,566,571,1675,571,1676,570,1676,598,1648,599,1648,598,1648,598,1649,597,1649,597,540,596,566,570,1676,570,566,570,567,569,568,569,1677,569,568,568,1678,569,1677,569,568,568,1678,568,1678,568,1678,568,568,569,1677,569,40054))
bargreen = array.array('H',(9072,4497,597,540,597,541,597,540,596,541,596,542,595,542,594,544,565,572,542,1706,540,1706,541,1705,541,1704,543,1703,543,1703,544,1702,570,1677,570,567,571,567,570,568,569,594,542,595,542,595,542,1705,542,596,541,1705,542,1706,541,1706,541,1706,541,1706,541,1705,542,596,541,1705,541,40091))
barblue = array.array('H',(9066,4527,567,570,596,540,598,540,597,540,596,541,596,541,594,543,566,571,542,1704,542,1704,541,1705,540,1705,541,1704,541,1705,541,1705,542,1704,542,1704,542,1704,542,594,543,594,567,570,543,594,542,1704,567,570,567,570,567,570,567,1679,568,1678,568,1679,567,1679,568,569,568,1678,568,40063))
barorange = array.array('H',(9132,4474,625,513,625,513,625,539,598,513,625,514,623,515,622,516,622,517,593,1680,543,1705,544,1704,543,1705,543,1705,543,1704,544,1704,543,1705,543,1705,544,1704,543,1705,543,594,569,569,569,569,569,568,569,569,569,568,570,568,569,569,570,1678,570,1678,569,1679,570,1678,569,1679,569,40082))
barlightgreen = array.array('H',(9116,4470,623,513,623,513,623,514,621,515,596,540,597,540,596,541,595,544,592,1653,593,1652,594,1676,570,1676,569,1677,569,1677,569,1677,569,1677,569,1677,569,568,568,1678,568,569,568,1678,568,569,568,568,568,569,567,569,568,1679,568,568,568,1679,568,569,567,1679,568,1678,568,1679,567,40071))
barlightblue = array.array('H',(9114,4470,622,514,622,514,621,515,594,542,594,542,570,566,570,566,570,566,569,1676,570,1676,569,1676,569,1676,569,1702,542,1703,542,1703,542,1703,542,1703,542,593,543,593,568,1677,568,568,568,567,569,567,569,567,569,567,568,1677,568,1677,568,568,568,1677,568,1677,568,1677,568,1677,568,40000))
baryellow = array.array('H',(9117,4467,625,511,625,511,625,512,624,511,625,512,624,512,625,511,624,513,598,1649,596,1674,571,1674,571,1675,571,1674,571,1675,570,1675,571,1675,570,566,570,1675,570,1676,569,567,569,1677,568,568,568,568,569,567,569,1677,568,568,569,567,569,1677,568,568,568,1677,569,1677,568,1677,569,40059))
barcycle = array.array('H',(9064,4524,569,566,570,566,571,566,570,566,570,567,570,566,570,566,570,566,570,1675,571,1675,570,1676,597,1649,598,1648,598,1649,597,1649,596,1649,597,1649,596,542,593,566,570,1676,569,1676,569,567,568,568,568,568,568,568,568,1677,569,1677,568,569,568,568,568,1678,568,1678,568,1678,568,40068))
barmagenta = array.array('H',(9067,4523,570,566,570,566,570,567,570,566,570,567,570,566,570,567,570,566,571,1676,570,1675,571,1675,598,1648,598,1647,598,1648,598,1648,598,1649,596,1650,596,542,594,1675,570,1676,570,566,569,568,569,567,569,568,568,569,568,1677,569,568,568,568,568,1678,569,1677,568,1678,568,1678,568,40059))
barrainbow = array.array('H',(9086,4493,598,537,599,537,599,537,599,537,600,536,625,511,626,511,625,511,625,1620,626,1620,624,1622,623,1622,599,1647,598,1648,597,1674,571,1674,571,565,571,565,571,565,570,1676,569,567,569,567,569,567,569,567,569,1677,569,1677,569,1676,569,567,569,1677,569,1676,569,1677,569,1676,569,40051))
barcolorswipe = array.array('H',(9116,4469,625,511,624,512,625,511,624,512,624,512,624,513,623,512,624,513,622,1624,596,1674,571,1675,570,1675,570,1675,571,1675,570,1675,571,1675,570,566,570,566,570,1676,569,1677,569,1676,569,568,568,568,568,568,568,1678,568,1677,568,568,568,568,568,568,568,1677,569,1676,569,1677,568,40061))
barcolorwave = array.array('H',(9110,4500,568,568,568,568,568,569,567,569,568,569,567,569,568,569,592,544,568,1679,568,1679,567,1680,567,1679,567,1680,567,1679,567,1680,567,1679,568,569,568,1679,567,570,567,1679,567,1680,567,569,567,1679,567,569,568,1678,568,569,567,1679,567,569,567,570,567,1678,568,569,567,1679,592,40016))

barcolors = [barred, bargreen, barblue, baryellow, barmagenta, barlightblue, barcycle, barorange, barlightgreen, barrainbow, barcolorswipe, barcolorwave]

def get_voltage(pin):
    #Does the correct scaling for 
    return (pin.value * 3.3) / 65536



if __name__ == "__main__":
    print(irmessage(0b100,1,0b1010,0b0101))