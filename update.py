#!/usr/bin/env python3
import os
from datetime import datetime

try:
	os.system("git clone https://github.com/Stef-deb/Version")
	os.system("mv Version/version.txt version.txt")
	os.system("rm -rf Version")
	os.system("rm -rf Gestionale")
	os.system("git clone https://github.com/Stef-deb/Gestionale")
	os.chdir("Gestionale")
	os.system("chmod +x gestionale.py")
	os.system("./gestionale.py")
except Exception as e:
	data = datetime.now()
	data = data.strftime("%D:%H:%M:%S")
	file = open("errors.txt", "a")
	file.write(f"\n{data}   {e}")
