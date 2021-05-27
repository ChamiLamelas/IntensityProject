@echo off
pip install numpy --disable-pip-version-check
pip install pandas --disable-pip-version-check
pip install pillow --disable-pip-version-check
pip list | findstr numpy
pip list | findstr pandas
pip list | findstr Pillow
echo check that numpy pandas and Pillow (with version) appear above
pause
