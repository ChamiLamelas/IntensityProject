@echo off
pip install numpy
pip install pandas
pip install pillow
pip list | findstr numpy
pip list | findstr pandas
pip list | findstr Pillow
echo check that numpy pandas and Pillow (with version) appear above
pause
