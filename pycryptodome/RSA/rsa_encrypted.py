# -*- coding: utf-8 -*-
"""
Created on Fri Nov 26 11:24:02 2021

@author: sbjkad
"""

import os
import rsa
import json
import hashlib
import base64
import sys
from Crypto import Cipher
from simple_settings import settings

class RSAEncrypter(object):
  """RSA加密解密
  参考 https://stuvel.eu/python-rsa-doc/index.html
  [description]
  """
  @classmethod
  def encrypt(cls, plaintext, keydata):
    #明文编码格式
    content = plaintext.encode('utf8')
    if os.path.isfile(keydata):
      with open(keydata) as publicfile:
        keydata = publicfile.read()
    pubkey = rsa.PublicKey.load_pkcs1_openssl_pem(keydata)
    #公钥加密
    crypto = rsa.encrypt(content, pubkey)
    return base64.b64encode(crypto).decode('utf8')
  @classmethod
  def decrypt(cls, ciphertext, keydata):
    if os.path.isfile(keydata):
      with open(keydata) as privatefile:
        keydata = privatefile.read()
    try:
      ciphertext = base64.b64decode(ciphertext)
      privkey = rsa.PrivateKey.load_pkcs1(keydata, format='PEM')
      con = rsa.decrypt(ciphertext, privkey)
      return con.decode('utf8')
    except Exception as e:
      pass
    return False
  @classmethod
  def signing(cls, message, privkey):
    from Crypto.Signature import pkcs1_15
    from Crypto.Hash import SHA256
    from Crypto.PublicKey import RSA
    if os.path.isfile(privkey):
      with open(privkey) as privatefile:
        privkey = privatefile.read()
    try:
      key = RSA.import_key(privkey)
      h = SHA256.new(message.encode('utf8'))
      sign = pkcs1_15.new(key).sign(h)
      sign = base64.b64encode(sign).decode('utf8')
      return sign
    except Exception as e:
      raise e
  @classmethod
  def verify(cls, message, sign, pubkey):
    from Crypto.Signature import pkcs1_15
    from Crypto.Hash import SHA256
    from Crypto.PublicKey import RSA
    res = False
    sign = base64.b64decode(sign)
    # print('sign', type(sign), sign)
    try:
      key = RSA.importKey(pubkey)
      h = SHA256.new(message.encode('utf8'))
      pkcs1_15.new(key).verify(h, sign)
      res = True
    except (ValueError, TypeError) as e:
      raise e
      pass
    except Exception as e:
      raise e
      pass
    return res

    secret = secret if secret else settings.default_aes_secret
    cipher = AESEncrypter(secret)
    encrypted = cipher.encrypt(plaintext)
    return '%s%s' % (prefix, encrypted)
if __name__ == "__main__":
  try:
    # for RSA test
    ciphertext = 'Qa2EU2EF4Eq4w75TnA1IUw+ir9l/nSdW3pMV+a6FkzV9bld259DxM1M4RxYkpPaVXhQFol04yFjuxzkRg12e76i6pkDM1itQSOy5hwmrud5PQvfnBf7OmHpOpS6oh6OQo72CA0LEzas+OANmRXKfn5CMN14GsmfWAn/F6j4Azhs='
    public_key = 'public.pem'
    private_key = 'private.pem'
    code_example = "import math\ndef floor(init,a):\n    limit = math.ceil((100 - init) / a)\n    for i in range(1,limit):\n        init = init+a\n        i = i+1\n    return(i + math.ceil(a/2))"
    ciphertext = RSAEncrypter.encrypt(code_example, public_key)
    print("ciphertext:\n", ciphertext)
    plaintext = RSAEncrypter.decrypt(ciphertext, private_key)
    print("plaintext:\n", plaintext)
  except KeyboardInterrupt:
    sys.exit(0)