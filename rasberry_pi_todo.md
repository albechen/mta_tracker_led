# ✅ What you already have (correct)

<https://github.com/hzeller/rpi-rgb-led-matrix>

sudo apt install python3-pil
git clone <https://github.com/hzeller/rpi-rgb-led-matrix.git>
cd rpi-rgb-led-matrix
make build-python
sudo make install-python

This:

Installs Pillow

Builds the Python bindings

Makes rgbmatrix importable

👍 Good.

1️⃣ Disable Raspberry Pi audio (required)

The RGB matrix uses PWM + DMA, which conflicts with audio.

Edit config:

sudo nano /boot/config.txt

Add or ensure this line exists:

dtparam=audio=off

Reboot after:

sudo reboot

If you skip this → flicker, random colors, or crashes.

2️⃣ You MUST run your script as root

The matrix uses DMA, which requires root.

❌ This will NOT work:

python3 display.py

✅ This WILL work:

sudo python3 display.py

(Or use sudo -E if you need env vars.)

5️⃣ Run from the repo at least once (recommended)

Test with the included demos before your own code:

cd rpi-rgb-led-matrix/examples-api-use
sudo python3 runtext.py --led-cols=64 --led-rows=32 --led-chain=2

If this doesn’t work:

Wiring

Power

Mapping
are not correct yet.

⚠️ Do this before debugging your script.

🔧 Optional but highly recommended tweaks
Reduce CPU usage
options.limit_refresh_rate_hz = 120

Reduce flicker
options.pwm_bits = 11

Lower brightness at night
matrix.brightness = 50  # 0–100
