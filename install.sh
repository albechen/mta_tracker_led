#!/bin/bash
set -e

echo "===== Updating system ====="
sudo apt update
sudo apt full-upgrade -y

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

cd bindings/python
sudo make install-python

echo "===== Installing Python packages ====="

cd "$HOME/mta_tracker_led"

pip3 install -r requirements.txt --break-system-packages

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