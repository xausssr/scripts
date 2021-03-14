'''
Скрипт для проведения аудита подключения USB устройств к компьютеру. 
Для построения отчета используется системный журнал. 
Записи вида *HCI Host Controller  не показываются т.к. являются системными. 
При необходимости вывода данных записей закомментировать соответствующий участок кода.
Выполнение скрипта только от суперпользователя (sudo)!

sudo python3 -m usb_seek

This work is licensed under 
MITLicense.

©Tolstykh A.A., 2021
'''

import os
import subprocess
import datetime as dt

p = subprocess.Popen("journalctl -q --output=short-unix | grep Serial | grep usb | grep SerialNumber:", stdout=subprocess.PIPE, stderr=None, shell=True)
byte_text = p.communicate()[0]
p.terminate()

text = byte_text.decode("utf-8").split("\n")[1:-1]

# поиск строк с usb
target_lines = []
for line in text:
    if " usb " in line:
        target_lines.append(line)

# выделение времени и серийного номера

usb_plugs = {}
for idx, line in enumerate(target_lines):
    temp = dt.datetime.fromtimestamp(int(line.split(".")[0]))
    usb_plugs[idx] = {}
    usb_plugs[idx]["time"] =  temp
    usb_plugs[idx]["serial"] = line.split("SerialNumber:")[1]


# выделение производителя и имени устройства

p = subprocess.Popen("journalctl -q --output=short-unix | grep usb | grep Manufacturer:", stdout=subprocess.PIPE, stderr=None, shell=True)
text_man = p.communicate()[0].decode("utf-8").split("\n")[1:-1]
p.terminate()

p = subprocess.Popen("journalctl -q --output=short-unix | grep usb | grep Product:", stdout=subprocess.PIPE, stderr=None, shell=True)
text_prod = p.communicate()[0].decode("utf-8").split("\n")[1:-1]
p.terminate()

products = {}
for line_man, line_prod in zip(text_man, text_prod):
	temp_man = dt.datetime.fromtimestamp(int(line_man.split(".")[0]))
	temp_line = dt.datetime.fromtimestamp(int(line_prod.split(".")[0]))
	if temp_man not in products.keys():
		products[temp_man] = (line_man.split("Manufacturer:")[1], line_prod.split("Product:")[1])

# добавление информации об устройствах
for idx in usb_plugs.keys():
	try:
		usb_plugs[idx]["Manufacturer"] = products[usb_plugs[idx]["time"]][0]
	except IndexError:
		usb_plugs[idx]["Manufacturer"] = "Unknown"

	try:
		usb_plugs[idx]["Product"] = products[usb_plugs[idx]["time"]][1]
	except IndexError:
		usb_plugs[idx]["Product"] = "Unknown"


# выделение сеанса пользователя
p = subprocess.Popen("journalctl -q --output=short-unix | grep login", stdout=subprocess.PIPE, stderr=None, shell=True)
byte_text = p.communicate()[0]
p.terminate()

text = byte_text.decode("utf-8").split("\n")[:-1]

logins = []
for line in text:
    if "New session" in line and "fly-dm" not in line:
        temp = dt.datetime.fromtimestamp(int(line.split(".")[0]))
        logins.append((temp, line.split(" ")[-1]))


# Соотнесение пользователя и флешки
for idx in usb_plugs.keys():
    usb_plugs[idx]["user"] = None
for idx_user in range(len(logins) - 1):
    for idx in usb_plugs.keys():
        if usb_plugs[idx]["time"] >= logins[idx_user][0] and usb_plugs[idx]["time"] < logins[idx_user + 1][0]:
            usb_plugs[idx]["user"] = logins[idx_user][1]

# последний активный сеанс
for idx in usb_plugs.keys():
    if usb_plugs[idx]["time"] >= logins[-1][0]:
        usb_plugs[idx]["user"] = logins[-1][1]

for idx_user in usb_plugs.keys():
    if usb_plugs[idx_user]["user"] is None:
        usb_plugs[idx_user]["user"] = "system"

# удаление системных сообщений
dropped_idx = []
for idx in usb_plugs.keys():
	if "HCI Host Controller" in usb_plugs[idx]["Product"]:
		dropped_idx.append(idx)

for i in dropped_idx:
	usb_plugs.pop(i, None)
 
# Красивый вывод

print("{:20s}|{:15s}|{:40s}|{:30s}|{:30s}".format("дата", "пользователь", "производитель", "модель", "серийный номер"))
print("-"* 20 + "|" + "-"* 15 + "|" + "-" * 40 + "|" + "-" * 30 + "|" + "-"* 30)
for line in usb_plugs.keys():
    print("{:20s}|{:15s}|{:40s}|{:30s}|{:30s}".format(usb_plugs[line]["time"].strftime("%Y.%m.%d %H:%M:%S"), usb_plugs[line]["user"], usb_plugs[line]["Manufacturer"], usb_plugs[line]["Product"], usb_plugs[line]["serial"]))
