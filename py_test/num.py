# -*- coding: utf-8 -*-
"""
Created on Mon Nov  1 15:13:59 2021

@author: sbjkad
"""

def fib(n):
    try:
        n = int(n)
        a, b = 0, 1
        while b < n:
            print(b)
            a,b = b,a + b
    except:
        print("it has to be an integer")

