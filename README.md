# NeopixelLiveMetroRailChennai
Neopixel - WS2812 LED Live Map

### Hardware List
- Raspberry Pi
- WS2812 Rounded Bullet LEDs (https://www.amazon.in/dp/B0FHDPV231?ref=ppx_pop_mob_ap_share)
- 5V 5Amp DC Power Supply
- Barrel Jack (For Easy connections) (https://www.amazon.in/dp/B09738N47R?ref=ppx_pop_mob_ap_share)
- Jumper Wires (https://www.amazon.in/dp/B07PQS67BN?ref=ppx_pop_mob_ap_share&th=1) 

### Software Setup
- Raspbian OS (Raspberry Pi official OS)
- Clone this repo for the code

#### Steps to Run

```
$> sudo pip3 install rpi_ws281x
$> sudo pip3 install adafruit-circuitpython-neopixel
$> sudo python3 -m pip install --force-reinstall adafruit-blinka
```

##### Run the test script to check all LEDs

Cycle through the GRB Colors - The LEDs support GRB instead of RGB depends on the LEDs you use
```
import time
import board
import neopixel

pixels1 = neopixel.NeoPixel(board.D18, 55, brightness=1)

pixels1.fill((0, 255, 0))
time.sleep(2)
pixels1[10] = (255, 0, 0)
time.sleep(2)
pixels1[10] = (0, 0, 255)
time.sleep(4)
pixels1.fill((0, 0, 0))
```

##### Run the crontab to start this on boot
```
crontab -e

#Add the below line to it
10 * * * * sudo python3 /path/to script
@reboot sudo python3 /path/to script
```

[Demo](https://youtube.com/shorts/eLv14lizPrQ?si=2FRvT8u8sRpRYZxp)

