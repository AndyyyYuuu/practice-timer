#!/bin/bash
TARGET=$(realpath practice.py)
sudo ln -sf "$TARGET" /usr/local/bin/practice
echo "Symlinked to /usr/local/bin/practice"