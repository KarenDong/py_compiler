# py_compiler
The <b>setup_all.py</b> will convert all .py file in selected folder to .pyd and delete the original files, the logic runs like below:
(1) Convert the original python program to C 
(2) Convert the c file to pyd in batch with cython 
(3) Delete the c file and the original python program

The <b>exptime.py</b> in test_py folder sets up a 30-days trail for sorce code. The logic is as below:
(1) On the first run, it will create a file with initial running time in it
(2) Afterwards, upon each run, the program will do the calculation first; if the running time minus the initial time is below 30 days, then the program will continues, otherwise it will exit.

## Instructions:
1. Navigate to the setup_all.py path in cmd
2. Run "python setup_all.py +absolute path"
python setup_all.py C:\Users\myname\Documents\Pycode\topyd\py_test
