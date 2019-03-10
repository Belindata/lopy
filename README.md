# LoPy/TTN Workshop

## Prerequisites

- LoPy/LoPy4/FiPy with Pysense/Pytrack and LoRa Antenna from [pycom](https://pycom.io)
- [TTN Account](https://account.thethingsnetwork.org)
- [IFTTT Account](https://ifttt.com)

## How To

- download repository to your computer
- open repository in Atom via `Add Project Folder...`
- rename desired python script to `main.py`
- add an application in the [TTN Console](https://console.thethingsnetwork.org/applications)
- add a device to your application, for this you will need the `device EUI` (see below)
- add `app_eui` and `app_key` in the script

### how to get your `device EUI`

- connect via REPL to your LoPy
- enter the following lines:

```
from network import LoRa
import binascii
lora = LoRa(mode=LoRa.LORAWAN)
print(binascii.hexlify(lora.mac()).upper().decode('utf-8'))
```

- the answer should look something like: `70B3D5499585FCA1`, copy this `device EUI`
