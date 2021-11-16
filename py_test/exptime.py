# -*- coding: utf-8 -*-
"""
Created on Tue Nov  2 10:59:01 2021

@author: sbjkad
"""

import os
import sys
import datetime
import num

first_launch_date_filepath = ".initial"


def is_program_expired():
# Query date of first lauch in given file
    if os.path.exists(first_launch_date_filepath):
        with open(first_launch_date_filepath, 'r') as fileRead:
            time_encode = fileRead.read()
            time_d = list(map(int,time_encode.split(",")))
            time_as_str = "".join(map(chr, time_d))
            start_date = datetime.datetime.strptime(time_as_str, "%Y_%m_%d")
            # Check if current time is greater than time limit
            expire_date = start_date + datetime.timedelta(days=31)
            if datetime.datetime.now() > expire_date:
                sys.exit("Your 1 month trial has expired.")
            else:
                diff = expire_date-datetime.datetime.now()
                print("Your trail still has "+str(diff.days)+" days left.")
    # first run
    else:
        start_date = datetime.datetime.now()
        start_date_str = start_date.strftime("%Y_%m_%d")
        ascii_list = list(map(ord,start_date_str))
        ascii_name = ",".join([str(x) for x in ascii_list])
        with open(first_launch_date_filepath, 'w') as fileWrite:
            fileWrite.write(ascii_name)
    
is_program_expired()        
m = input("input(it has to be an integer):")
num.fib(m)


#now()
#if now() > s:
#    print('Your 1 month trial has expired.')
#else:
#    m = input("input(it has to be an integer):")
#    num.fib(m)