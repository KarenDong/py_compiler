# -*- coding: utf-8 -*-
"""
Created on Fri Nov 26 12:50:07 2021

@author: sbjkad
"""
from Crypto.PublicKey import RSA
from Crypto.Random import get_random_bytes
from Crypto import Cipher
from Crypto.Cipher import AES, PKCS1_OAEP


key = RSA.generate(2048)
private_key = key.export_key()
file_out = open("private.pem", "wb")
file_out.write(private_key)
file_out.close()

public_key = key.publickey().export_key()
file_out = open("public.pem", "wb")
file_out.write(public_key)
file_out.close()