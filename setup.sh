#!/bin/bash

echo "Starting Cloud Project Setup..."

#packages
echo "Updating system..."
sudo apt update && sudo apt upgrade -y

#dependencies
echo "Installing Python3 and Docker..."
sudo apt install -y python3 python3-pip python3-venv docker.io

#docker
sudo systemctl start docker
sudo systemctl enable docker

#virtual environment
echo "Creating Python virtual environment..."
python3 -m venv venv

#venv and install packages
echo "Installing Python packages inside venv..."
source venv/bin/activate
pip install --upgrade pip
pip install pyqt5 psutil bcrypt matplotlib

deactivate

#permissions (optional)
chmod +x atkGUI.py defGUI.py

echo "Setup complete!"
echo "Run 'source venv/bin/activate' before using the GUI:"
echo "   python3 atkGUI.py"
echo "   python3 defGUI.py"
