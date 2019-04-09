from pytrack import Pytrack
# from pysense import Pysense
from LIS2HH12 import LIS2HH12
import pycom
from network import LoRa
import binascii
import time
import socket
import ustruct

# for Pytrack shield
py = Pytrack()

# for Pysense shield
# py = Pysense()

# initialize acceleration sensor
lis = LIS2HH12(py)

# stop heartbeat (blue flashing led) and show red
pycom.heartbeat(False)
pycom.rgbled(0x7f0000) # red

# initialize LoRa
lora = LoRa(mode=LoRa.LORAWAN)

# app_eui and app_key from TTN console
app_eui = binascii.unhexlify('')
app_key = binascii.unhexlify('')

# join the LoRa network
lora.join(activation=LoRa.OTAA, auth=(app_eui, app_key), timeout=0)

# wait until the module has joined the network
while not lora.has_joined():
    time.sleep(2.5)
    print('Not joined yet...')

print('Network joined!')

# signalize join by green and after 2 seconds turn off led
pycom.rgbled(0x007f00) # green
time.sleep(2)
pycom.rgbled(0x000000) # turn off

# create a LoRa socket
s = socket.socket(socket.AF_LORA, socket.SOCK_RAW)

# set the LoRaWAN data rate
s.setsockopt(socket.SOL_LORA, socket.SO_DR, 5)

# loop until module is tilted over the threshold
while(True):

    # read acceleration (tuple of three)
    acc = lis.acceleration()

    # print current readings to REPL
    print("x: " + str(acc[0]) + ", y: " + str(acc[1]) + ", z: " + str(acc[2]))

    # if module is tilted over the threshold
    if(acc[2] < 0.9):

        # show blue led
        pycom.rgbled(0x00007f) # blue

        # pack acceleration readings into three shorts (two bytes each)
        # + 32758 brings also negative values in the positive range
        # unpacked in TTN backend via custom decoder
        acc_bytes = ustruct.pack('hhh', int(10000 * acc[0] + 32768), int(10000 * acc[1] + 32768), int(10000 * acc[2] + 32768))

        # block socket, send bytes and unblock socket
        s.setblocking(True)
        s.send(acc_bytes)
        s.setblocking(False)

        # wait before turning off led and exit of loop
        time.sleep(5)
        pycom.rgbled(0x000000) # turn off
        break

    # wait before next reading
    time.sleep(1)
