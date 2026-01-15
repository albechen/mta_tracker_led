# RASPBERRY PI SETUP

## INTIAL SET UP

### RASPBERRY PI IMAGER

FONTS: <https://www.cl.cam.ac.uk/~mgk25/ucs-fonts.html>
imager to 64bit and bookworm version
PYTHON 3.11 recc

### UPDATE AND CONFIGURE

```bash
sudo apt update && sudo apt full-upgrade -y
sudo raspi-config - vnc on

sudo sed -i 's/^dtparam=audio=.*/dtparam=audio=off/' /boot/firmware/config.txt
echo "blacklist snd_bcm2835" | sudo tee /etc/modprobe.d/blacklist-alsa.conf
echo "blacklist snd_soc_hdmi_codec" | sudo tee -a /etc/modprobe.d/blacklist-alsa.conf
echo "blacklist snd_soc_core" | sudo tee -a /etc/modprobe.d/blacklist-alsa.conf
echo "blacklist snd_pcm" | sudo tee -a /etc/modprobe.d/blacklist-alsa.conf
```

```bash
sudo nano /boot/cmdline.txt
```

At the end of long line, add a space and: isolcpus=3

Ctrl+O **to write**
Ctrl+X **to exit**

```bash
sudo reboot
```

### TEMP TURN AUDIO OFF

```bash
sudo rmmod snd_bcm2835
sudo nano /boot/firmware/config.txt dtparam=audio=off
```

## INSTALL LED SPECIFIC LIBRARIES

### INSTALL RPI-RGB-led-matrix

```bash
git clone https://github.com/hzeller/rpi-rgb-led-matrix
cd rpi-rgb-led-matrix
make
pip install . --break-system-packages
```

### INSTALL PYTHON BINDINGS

```bash
cd bindings/python
sudo apt-get update && sudo apt-get install python3-dev cython3 -y
make build-python
sudo make install-python
```

## TEST CASES

### check if python bindings installed

```bash
python3 - << 'EOF'
from rgbmatrix import RGBMatrix
print("OK")
EOF
```

### check c++ demo

```bash
cd ~/rpi-rgb-led-matrix/examples-api-use
sudo ./demo -D0 --led-rows=32 --led-cols=64 --led-gpio-mapping=adafruit-hat
```

### CREATE TEST CASE CHECK EACH PIXEL

```bash
nano ~/test_led.py
```

```bash
#!/usr/bin/env python3

import time
from rgbmatrix import RGBMatrix, RGBMatrixOptions

# Matrix options
options = RGBMatrixOptions()
options.rows = 32
options.cols = 64
options.chain_length = 1
options.parallel = 1
options.hardware_mapping = "adafruit-hat-pwm"
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
```

Ctrl+O **to write**
Ctrl+X **to exit**

```bash
sudo python3 ~/test_led.py
```

## DOWNLOAD LIBRARIES SPECIFIC

```bash
sudo python3 -m pip install requests pillow gtfs-realtime-bindings --break-system-packages

python -c "import requests; print('requests OK')"
python -c "from google.transit import gtfs_realtime_pb2; print('gtfs OK')"
```

## HOW TO RUN PROJECT

### to intially clone on pi

```bash
git clone https://github.com/albechen/mta_tracker_led
sudo chown -R root:root /home/trackthemta/mta_tracker_led
sudo chmod -R 777 /home/trackthemta/mta_tracker_led/assets/led_matrix_render
cd mta_tracker_led
```

### to pull new version on pi

```bash
cd ~/mta_tracker_led
git pull

sudo systemctl stop ledmatrix.service
cd ~/mta_tracker_led
sudo git pull
sudo systemctl start ledmatrix.service
```

### Delete pre-render

```bash
cd ~/mta_tracker_led/assets/led_matrix_render
rm pre_render*.png
cd
```

### to run it

```bash
cd mta_tracker_led
sudo python main.py
```

### CONNECT

```bash
ssh trackthemta@trackthemta
```

## Install start program on power on

```bash
cd ~/mta_tracker_led
pwd
```

OUTPUT: /home/trackthemta/mta_tracker_led
So full path: /home/trackthemta/mta_tracker_led/main.py

### Create Start Service

```bash
cd
sudo nano /etc/systemd/system/ledmatrix.service
```

Paste below in service file
Save: CTRL+O → Enter → CTRL+X

```ini
[Unit]
Description=MTA Tracker LED Matrix Python
After=network.target

StartLimitBurst=30
StartLimitIntervalSec=630

[Service]
ExecStart=/usr/bin/python3 /home/trackthemta/mta_tracker_led/main.py
WorkingDirectory=/home/trackthemta/mta_tracker_led
StandardOutput=journal
StandardError=journal
Restart=always
RestartSec=5

User=root

# Allow hardware access
Environment=DISPLAY=:0

[Install]
WantedBy=multi-user.target
```

### Create Stop Service

```bash
sudo nano /etc/systemd/system/ledmatrix-stop.service
```

Save: CTRL+O → Enter → CTRL+X

``` ini
[Unit]
Description=Stop MTA Tracker LED Matrix

[Service]
Type=oneshot
ExecStart=/bin/systemctl stop ledmatrix.service
```

### Create Timers

#### START

```bash
sudo nano /etc/systemd/system/ledmatrix.timer
```

Save: CTRL+O → Enter → CTRL+X

``` ini
[Unit]
Description=Start LED Matrix at 07:00

[Timer]
OnCalendar=*-*-* 07:00:00
Persistent=true
Unit=ledmatrix.service

[Install]
WantedBy=timers.target
```

#### STOP

```bash
sudo nano /etc/systemd/system/ledmatrix-stop.timer
```

Save: CTRL+O → Enter → CTRL+X

``` ini
[Unit]
Description=Stop LED Matrix at 00:00

[Timer]
OnCalendar=*-*-* 00:00:00
Persistent=true
Unit=ledmatrix-stop.service

[Install]
WantedBy=timers.target
```

### Set up journal to only keep a day's data

```bash
sudo nano /etc/systemd/journald.conf
```

``` ini
MaxRetentionSec=1day
```

```bash
sudo systemctl restart systemd-journald
```

clear logs more than a day

```bash
sudo journalctl --vacuum-time=1d
journalctl --disk-usage
```

### Enable + start the service

```bash
sudo systemctl daemon-reload
sudo systemctl enable  --now ledmatrix.service
sudo systemctl enable --now ledmatrix.timer
sudo systemctl enable --now ledmatrix-stop.timer
```

Check if it is running

```bash
sudo systemctl status ledmatrix.service
```

```bash
sudo reboot
```

### Check print / Stop / disable

Stream of print statments (Ctrl+C to exit):

```bash
sudo systemctl stop ledmatrix.service
cd ~/mta_tracker_led
sudo git pull
cd
sudo systemctl start ledmatrix.service
sudo journalctl -u ledmatrix.service -f

```

```bash
journalctl -u ledmatrix.service
sudo systemctl status ledmatrix.service
sudo journalctl -u ledmatrix.service -f
journalctl -u ledmatrix.service --since "15 min ago"
```

restart

```bash
sudo systemctl daemon-reload
sudo systemctl restart ledmatrix.service
```

Stop or diable

```bash
sudo systemctl stop ledmatrix.service
sudo systemctl disable ledmatrix.service
```
