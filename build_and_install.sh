#!/bin/bash
set -e

echo "Building Swift paste helper..."
swiftc -O paste_helper.swift -o paste_helper_type
sudo cp paste_helper_type /tmp/paste_helper_type

echo "Installing Python dependencies..."
pip3 install pynput mlx-whisper mlx rumps pyperclip

echo "Done! You can now run the app:"
echo "python3 DictationApp.py"
