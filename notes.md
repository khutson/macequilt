screen /dev/ttyUSB0 115200

esptool.py --port /dev/ttyUSB0 erase_flash

esptool.py --port /dev/ttyUSB0 --baud 460800 write_flash --flash_size=detect -fm dio 0 esp8266-20171101-v1.9.3.bin 



esp8285:

esptool.py --port /dev/ttyUSB0 --baud 115200 write_flash -fm dout -fs 1MB 0x00000 esp8266-20171101-v1.9.3.bin 


esp32:

esptool.py --chip esp32 --port /dev/ttyUSB1 write_flash -z 0x1000 firmware.bin
