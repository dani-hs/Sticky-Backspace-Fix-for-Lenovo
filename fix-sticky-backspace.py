#!/usr/bin/python

from evdev import InputDevice
from evdev.ecodes import EV_KEY, KEY_BACKSPACE, EV_SYN, SYN_REPORT
from select import select
from time import sleep

kbd = InputDevice('/dev/input/event4') # Here we have to chose the right input device

print(kbd)


#---- Begin of quirk ----------------------------------------------------------------------------
#---- This quirk is used to fix swapped kbd.repeat.delay and kbd.repeat.repeat in python-evdev
#---- When the issue is fixed in evdev this quirk can be removed
from evdev import _input
from collections import namedtuple
_KbdInfo = namedtuple("KbdInfo", ["delay", "repeat"])
del InputDevice.repeat
InputDevice.repeat = property(lambda self: _KbdInfo(*_input.ioctl_EVIOCGREP(self.fd)))
#---- End of quirk -------------------------------------------------------------------------------




v = 0 if KEY_BACKSPACE in kbd.active_keys() else 1  #value of backspace key: up=0, down=1, hold=2 (for the inital value it's not possible and not that important to distiguish between down an hold)

"""
returns if any backspace key event was read
"""
def read(timeout = None):
	global v
	res = False
	r, _, _ = select([kbd.fd], [], [], timeout)#Wait for input
	if r:
		for ev in kbd.read():
			if ev.type == EV_KEY and ev.code == KEY_BACKSPACE:
				v = ev.value
				res = True
#				print(v,res)
	return res
		
while True:
	if v == 1:
		sleep(kbd.repeat.delay / 1000)
		if not read(0.001):
			kbd.write(EV_KEY, KEY_BACKSPACE, 0)
			kbd.write(EV_SYN, SYN_REPORT, 0)
	elif v == 2:
		sleep(kbd.repeat.repeat / 1000)
		if not read(0.001):	
			kbd.write(EV_KEY, KEY_BACKSPACE, 0)
			kbd.write(EV_SYN, SYN_REPORT, 0)	
	else:
		read()

