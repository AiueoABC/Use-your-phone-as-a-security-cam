# Use-your-phone-as-a-security-cam
Experimental repo. I made this to play with Termux, so I did tons of stupid things.
This repo works with Termux app and Termux-api app in your phone.
Using TCP/IP to send/receive camera images remotely.

## Codes for phone (Sender)
1) Photo_with_subprocess.py
 This script calls "termux-camera-photo" of Termux-api and save temporary file once.
 After saving it, it's possible to send photo data to other terminals.
 (Change 'host_name' and 'port_name' as you wish)

2) Photo_with_subprocess2_continuous.py
 Continuous version of first one. Use with the script "photoreceiver2_continuous.py".
 (Change 'host_name' and 'port_name' as you wish)
 
 ## Codes for terminal (Receiver)
 1) photoreceiver.py
   Use with "Photo_with_subprocess.py". (Change 'host_name' and 'port_name' as you wish)

 2) Photo_with_subprocess2_continuous.py
   Use with "Photo_with_subprocess.py". (Change 'host_name' and 'port_name' as you wish)

# Requirements
Please confirm following things for phones and for terminals are OK.
## For phones
### Requirements
Termux, Termux:API, python(on Termux), numpy(on Termux), OpenCV(on Termux)

### Installations
  First of first, you need to install following things;
   1) Install Termux (Follow the instructions here: https://termux.com/)
   2) Install Termux:API (Follow the instructions here: https://wiki.termux.com/wiki/Termux:API)
  
  After installing these, you need to do followings in the terminal of Termux app;
   1) Upgrade packages with "pkg upgrade"
   2) Get access to the storage with "termux-setup-storage" ('Storage' directory will appear)
   3) Install python with "pkg install python"
   4) Get its-pointless repo (Follow the instructions here: https://wiki.termux.com/wiki/Package_Management#By_its-pointless_.28live_the_dream.29:)
   5) Install scipy with "pkg install scipy"
   6) Install OpenCV (Follow the instructions here: https://wiki.termux.com/wiki/Instructions_for_installing_python_packages#opencv)

## For terminals
### Requirements
Python, numpy, OpenCV
