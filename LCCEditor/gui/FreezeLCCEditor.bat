:: The python initialization file for pylet imports several modules unneeded for the LCC Editor.
:: This causes the frozen distribution folder for the Editor to be unnecessarily large.
:: To prevent this, a temporary initialization file that eliminates the unnecessary imports
:: is swapped with the __init__.py file before running the freeze command. After freezing,
:: the __init__.py file is swapped back.
::
d:
cd \ATtILA2\src\pylet\pylet
::
rename __init__.py original_init.bak
rename freeze_init.bak __init__.py
::
cd \ATtILA2\src\LCCEditor\LCCEditor\gui
start /WAIT cxfreeze __init__.py --target-dir bin --target-name LCCEditor.exe --base-name Win32GUI --include-modules atexit,PySide.QtNetwork --exclude-modules arcpy,pylet.arcpyutil,pylet.conversion,pylet.datetimeutil,pywintypes
copy LCCEditor.pyw .\bin\LCCEditor.pyw
::
cd \ATtILA2\src\pylet\pylet
rename __init__.py freeze_init.bak
rename original_init.bak __init__.py
exit