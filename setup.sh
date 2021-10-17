#!/bin/bash
task(){
    $@ &>/dev/null
}
task rm -r /tmp/apt/state/lists
echo "Installing Python 3.9..."
task install-pkg python3.9
echo "Installing Python dist utils..."
task install-pkg python3.9-distutils
#echo "Installing Tesseract..."
#task install-pkg tesseract -y
echo "Done!"
echo "Installing dependencies..."
task python3.9 -m pip install --force-reinstall psutil
task python3.9 -m pip install -r requirements.txt
echo "Done!"
task python3.9 ./setup.py
