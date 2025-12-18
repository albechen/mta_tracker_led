### RASPBERRY PI IMAGER ###
FONTS: https://www.cl.cam.ac.uk/~mgk25/ucs-fonts.html
imager to 64bit and bookworm version
PYTHON 3.11 recc

### SET UP RASPBERRY PI ###
sudo apt update && sudo apt full-upgrade -y
sudo raspi-config - vnc on

sudo nano /boot/firmware/config.txt dtparam=audio=off

sudo nano /boot/cmdline.txt
At the end of long line, add a space and: isolcpus=3
Ctrl+O **to write**
Ctrl+X **to exit**

sudo reboot

### INSTALL RPI-RGB-LED-MATRIX ###
git clone https://github.com/hzeller/rpi-rgb-led-matrix
cd rpi-rgb-led-matrix
make
pip install . --break-system-packages


### INSTALL PYTHON BINDINGS ###
cd bindings/python
sudo apt-get update && sudo apt-get install python3-dev cython3 -y
make build-python
sudo make install-python

### TESTING CASES ###

# check if python bindings installed
python3 - << 'EOF'
from rgbmatrix import RGBMatrix
print("OK")
EOF

# check c++ demo
cd ~/rpi-rgb-led-matrix/examples-api-use
sudo ./demo -D0 --led-rows=32 --led-cols=64 --led-gpio-mapping=adafruit-hat


### CREATE TEST CASE CHECK EACH PIXEL ###
nano ~/test_led.py

#!/usr/bin/env python3

import time
from rgbmatrix import RGBMatrix, RGBMatrixOptions

# Matrix options
options = RGBMatrixOptions()
options.rows = 32
options.cols = 64
options.chain_length = 1
options.parallel = 1
options.hardware_mapping = "adafruit-hat"
options.brightness = 40

matrix = RGBMatrix(options=options)

# Colors to display
colors = [
    (255, 0, 0),       # Red
    (0, 255, 0),       # Green
    (0, 0, 255),       # Blue
    (255, 255, 0),     # Yellow
    (255, 255, 255),   # White
]

try:
    for r, g, b in colors:
        for x in range(64):
            for y in range(32):
                matrix.SetPixel(x, y, r, g, b)
        time.sleep(2)
finally:
    matrix.Clear()


Ctrl+O **to write**
Ctrl+X **to exit**

sudo python3 ~/test_led.py


### DOWNLOAD LIBRARIES IN VENV ###

sudo apt update
sudo apt install -y python3 python3-pip python3-venv python3-dev

python3 -m venv venv

# active venv

source venv/bin/activate
** should see (venv) pi@raspberrypi:~ $ **

pip install --upgrade pip setuptools wheel
pip install requests pillow gtfs-realtime-bindings

python -c "import requests; print('requests OK')"
python -c "from google.transit import gtfs_realtime_pb2; print('gtfs OK')"


### HOW TO RUN PROJECT ###

source venv/bin/activate
sudo python main.py