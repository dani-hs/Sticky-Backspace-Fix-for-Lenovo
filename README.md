Some Lenovo Notebooks have a second backspace key on top of the keypad.
For this backspace key the key down and key hold scancodes were generated.
But the key up scancodes were missing (perhaps due to a hardware or firmware bug).

In several programms (gnome for example) this leads to the impression that the secondary backspace key is sticky.

This script adds the missing key up events. Thus a normal user expierience is achieved.
