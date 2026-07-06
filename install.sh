#!/bin/bash
set -e

echo "===== Updating system ====="
sudo apt update
sudo apt full-upgrade -y

echo "===== Mute Audio ====="

sudo sed -i 's/^dtparam=audio=.*/dtparam=audio=off/' /boot/firmware/config.txt
echo "blacklist snd_bcm2835" | sudo tee /etc/modprobe.d/blacklist-alsa.conf
echo "blacklist snd_soc_hdmi_codec" | sudo tee -a /etc/modprobe.d/blacklist-alsa.conf
echo "blacklist snd_soc_core" | sudo tee -a /etc/modprobe.d/blacklist-alsa.conf
echo "blacklist snd_pcm" | sudo tee -a /etc/modprobe.d/blacklist-alsa.conf

sudo rmmod snd_bcm2835
sudo nano /boot/firmware/config.txt dtparam=audio=off


echo "===== Installing packages ====="
sudo apt install -y \
git \
build-essential \
python3-pip \
python3-dev \
cython3


echo "===== Downloading RGB Matrix library ====="

if [ ! -d "$HOME/rpi-rgb-led-matrix" ]; then
    git clone https://github.com/hzeller/rpi-rgb-led-matrix.git "$HOME/rpi-rgb-led-matrix"
fi

cd "$HOME/rpi-rgb-led-matrix"

make
pip install . --break-system-packages


echo "===== Installing Python Binds ====="

cd bindings/python
sudo apt-get update && sudo apt-get install python3-dev cython3 -y
make build-python
sudo make install-python


echo "===== Installing Python packages ====="

cd "$HOME/mta_tracker_led"

pip3 install -r requirements.txt --break-system-packages

python -c "import requests; print('requests OK')"
python -c "from google.transit import gtfs_realtime_pb2; print('gtfs OK')"

echo "Installing systemd files..."

sudo cp systemd/* /etc/systemd/system/

sudo systemctl daemon-reload

sudo systemctl enable ledmatrix.service
sudo systemctl enable ledmatrix-start.timer
sudo systemctl enable ledmatrix-stop.timer

echo ""
echo "Installation complete."
echo "Reboot with:"
echo "sudo reboot"