# -*- coding: utf-8 -*-
"""
Created on Tue Nov  9 16:59:12 2021

@author: sbjkad
"""

import os
import shutil
import time
import sys

def func(path):
    folder_path = os.path.dirname(path)
    file_path = os.path.split(path)[1]
    print(path)
    print(file_path)
    os.chdir(folder_path)
    with open('setup.py', 'w') as f:
        f.write('from setuptools import setup\n')
        f.write('from Cython.Build import cythonize\n')
        f.write('setup(\n')
        f.write("name='test',\n")
        f.write("ext_modules=cythonize('%s')\n" % file_path)
        f.write(")\n")
    os.system('python setup.py build_ext --inplace')
    filename = file_path.split('.py')[0]
    print(filename)
    time.sleep(2)
    os.remove('%s.c' % filename)
    
    build_folder_path = os.path.join(folder_path, 'build')
    shutil.rmtree(build_folder_path)
    os.remove('setup.py')
    os.remove(file_path)
    
def get_all_file(path):
    for root, dirs, files in os.walk(path):
        for name in files:
            if name.endswith(".py"):
                file_path = os.path.join(root, name)
                func(file_path)
                
paths = sys.argv[1]
get_all_file(paths)