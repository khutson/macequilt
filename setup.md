# Setup

## USB setup
There's a good tutorial at <https://www.pololu.com/docs/0J7/all>

## burning micropython onto the ESP32 ESP8266, or ESP8285

### python3
You'll need to install python. If you don't already have it, I recommend the anaconda distribution. 
<https://www.anaconda.com/download/>
Make sure you get python3.

Set up a virtual environment named "mp" (for micropython):

    conda env create -n mp python=3

This helps keep the micropython tools separate from any other python projects.

To install the python tools from the command line:

    pip install adafruit-ampy esptool

### flash micropython
Download the latest image from <http://micropython.org/download#esp8266>

#### esp8266:

    esptool.py --port /dev/ttyUSB0 erase_flash
    esptool.py --port /dev/ttyUSB0 --baud 460800 write_flash --flash_size=detect -fm dio 0 esp8266-20171101-v1.9.4.bin 


##### esp8285:
Uses same image as the ESP8266.

    esptool.py --port /dev/ttyUSB0 --baud 115200 write_flash -fm dout -fs 1MB 0x00000 esp8266-20171101-v1.9.4.bin 


#### esp32:
Download from <http://micropython.org/download#esp32>

    esptool.py --chip esp32 --port /dev/ttyUSB1 write_flash -z 0x1000 esp32-20180511-v1.9.4.bin


### Connect to the ESPxx

You'll need a terminal program like [Putty for windows](https://www.putty.org/), or screen for linux

*linux*


    sudo apt-get install screen

to find the right serial port:

    ls /dev/ttyUSB*

It's usually /dev/ttyUSB0 or /dev/ttyUSB1.
To connect to the ESPxx:

    screen /dev/ttyUSB0 115200


## micropython development tools

There are a few to choose from, but none that are perfect, in my opinion.
Try starting with uPyCraft.
ESPlorer with the micropython additions is also pretty good.
Neither one will give you a fancy editor like one of the big python IDE's, but they'll definitely get you started.

To run ESPlorer, `java -jar ESPlorer.jar`

## connecting to wifi

Using your chosen tool, copy the files in the workSpace directory to the ESPxx. 
You may need to edit the wificonfig.py file to add your wifi network if you're not working at the MAC.

## micropython libraries

Once you've connected to the ESPxx with a terminal program or one of the dev tools, run `artsetup.py`.
That will try to install the libraries we need for the project.
