# pc-control
Simple server that can run certain commands on computer and can be called from Google Home.

You can use it with http://github.com/mhozza/pi-control.

## Instalation

Requires python 3.6+

### Linux

```bash
sudo pip install -r requirements.txt
sudo ./install.py
```

### Windows

Install requirements globally using admin rights:
```
pip install -r requirements.txt
pip install -r requirements_win.txt
```

Be sure to have the file C:\Program Files\Python36\Lib\site-packages\win32\pywintypes36.dll (please note that “36” is the version of your Python installation). If you don’t have this file, take it from C:\Program Files\Python36\Lib\site-packages\pywin32_system32\pywintypes36.dll and copy it into C:\Program Files\Python36\Lib\site-packages\win32

```
.\install.py
```
