# CSC1010

RASPI SETUP
=======================
1) Install python: sudo apt install python3 idle3
2) Install pip: sudo apt-get install python-pip
3) Install nodejs: sudo apt install nodejs
4) Install Socket.IO: npm install socket.io --save
5) Install MQTT: pip install paho-mqtt
6) Create project folder: mkdir FOLDER_NAME
7) Repeat 1) to 6) in the second raspberry pi
8) Use scp command to transfer room.py to the created folder in the first raspberry pi
9) Use scp command to transfer kitchen.py to the created folder in the second raspberry pi
10) Run room.py in first raspberry pi: python room.py
11) Run kitchen.py in second raspberry pi: python kitchen.py


Resources
======================
https://www.youtube.com/watch?v=TVxQROFPjy0
get host IP: hostname -I
