@echo off
mode con:cols=80 lines=24
color 0a
pip3 -qqq install requests console-menu terminalplot > NUL
python3 ocsexplorer.py
color