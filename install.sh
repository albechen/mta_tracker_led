#!/bin/bash
set -e

echo "===== Give acess everything ====="
sudo mkdir -p /home/trackthemta/mta_tracker_led/assets/led_matrix_render
sudo chown -R root:root /home/trackthemta/mta_tracker_led/assets
sudo chmod -R 755 /home/trackthemta/mta_tracker_led/assets
sudo chmod 777 /home/trackthemta/mta_tracker_led/assets/led_matrix_render

echo "===== Updating system ====="
sudo apt update
sudo apt full-upgrade -y

echo "===== Mute Audio ====="
grep -q 'isolcpus=3' /boot/firmware/cmdline.txt || sudo sed -i 's/$/ isolcpus=3/' /boot/firmware/cmdline.txt
grep -q 'isolcpus=3' /boot/cmdline.txt || sudo sed -i 's/$/ isolcpus=3/' /boot/cmdline.txt

sudo sed -i 's/^dtparam=audio=.*/dtparam=audio=off/' /boot/firmware/config.txt
echo "blacklist snd_bcm2835" | sudo tee /etc/modprobe.d/blacklist-alsa.conf
echo "blacklist snd_soc_hdmi_codec" | sudo tee -a /etc/modprobe.d/blacklist-alsa.conf
echo "blacklist snd_soc_core" | sudo tee -a /etc/modprobe.d/blacklist-alsa.conf
echo "blacklist snd_pcm" | sudo tee -a /etc/modprobe.d/blacklist-alsa.conf

sudo rmmod snd_bcm2835


echo "===== Installing packages ====="
sudo apt install -y \
git \
build-essential \
python3-pip \
python3-dev \
cython3


echo "===== Downloading RGB Matrix library ====="

sudo apt-get install python-dev-is-python3 python3-pil cython3

if [ ! -d "$HOME/rpi-rgb-led-matrix" ]; then
    git clone https://github.com/hzeller/rpi-rgb-led-matrix.git "$HOME/rpi-rgb-led-matrix"
fi

cd "$HOME/rpi-rgb-led-matrix"

make
sudo pip3 install . --break-system-packages
sudo python3 -c "from rgbmatrix import RGBMatrix; print('OK')"

echo "===== Installing Python Binds ====="

cd bindings/python
sudo apt-get update && sudo apt-get install python3-dev cython3 -y
make build-python
sudo make install-python


echo "===== Installing Python packages ====="

cd "$HOME/mta_tracker_led"

# pip3 install -r requirements.txt --break-system-packages
sudo python3 -m pip install requests pillow gtfs-realtime-bindings --break-system-packages

python -c "import requests; print('requests OK')"
python -c "from google.transit import gtfs_realtime_pb2; print('gtfs OK')"


echo "===== Installing temperature watchdog ====="

sudo apt install -y bc
sudo cp scripts/temp_shutdown.sh /usr/local/bin/
sudo chmod +x /usr/local/bin/temp_shutdown.sh


echo "===== Installing systemd files ====="

sudo cp systemd/*.service /etc/systemd/system/
sudo cp systemd/*.timer /etc/systemd/system/


echo "===== Configuring journal limits ====="

sudo mkdir -p /etc/systemd/journald.conf.d

sudo tee /etc/systemd/journald.conf.d/mta-led.conf > /dev/null <<EOF
[Journal]
Storage=persistent
SystemMaxUse=50M
SystemMaxFileSize=5M
MaxRetentionSec=1day
EOF

sudo systemctl restart systemd-journald


echo "===== Reloading systemd ====="

sudo systemctl daemon-reload


echo "===== Enabling services ====="

sudo systemctl enable ledmatrix.service
sudo systemctl enable ledmatrix-start.timer
sudo systemctl enable ledmatrix-stop.timer
sudo systemctl enable temp-shutdown.timer


echo ""
echo "======================================"
echo "Installation complete."
echo "Reboot with:"
echo "sudo reboot"
echo "======================================"