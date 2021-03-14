# Scripts
Various scripts for administration/forensic.

## Useful links

* [Astra Linux user creation automatisation](https://github.com/yurylunev/astra-script) by [yurylunev](https://github.com/yurylunev)
   * > Скрипт автоматического создания пользователей в ОС Astra Linux.
* [usbrip](https://github.com/snovvcrash/usbrip) by [snovvcrash](https://github.com/snovvcrash)
   * > usbrip (inherited from "USB Ripper", not "USB R.I.P.") is a simple forensics tool with command line interface that lets you keep track of USB device artifacts (i.e., USB event history) on Linux machines.  

## usb_seek

Script for parsing system journals and get USB plugs events for audit. 
Example of usage:

```sudo python3 -m usb_seek```

* No additional dependencies are needed for this script.
* Tested on 
  * Astra Linux
  * Kali Linux
  * Ubuntu 20.04
  * Kali Linux (VirtualBox)

Example of output:

![image](https://user-images.githubusercontent.com/12968086/111060681-c7227700-84af-11eb-8cb9-e4fdee86dbe0.png)
