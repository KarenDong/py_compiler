from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
import hashlib
import base64
from simple_settings import settings
import datetime
import wmi
import sys

class AESEncrypter(object):
  def __init__(self, key, iv=None):
    self.key = key.encode('utf8')
    self.iv = iv if iv else bytes(key[0:16], 'utf8')
  def _pad(self, text):
    text_length = len(text)
    padding_len = AES.block_size - int(text_length % AES.block_size)
    if padding_len == 0:
      padding_len = AES.block_size
    t2 = chr(padding_len) * padding_len
    t2 = t2.encode('utf8')
    # print('text ', type(text), text)
    # print('t2 ', type(t2), t2)
    t3 = text + t2
    return t3
  def _unpad(self, text):
    pad = ord(text[-1])
    return text[:-pad]
  def encrypt(self, raw):
    raw = raw.encode('utf8')
    raw = self._pad(raw)
    cipher = AES.new(self.key, AES.MODE_CBC, self.iv)
    encrypted = cipher.encrypt(raw)
    return base64.b64encode(encrypted).decode('utf8')
  def decrypt(self, enc):
    enc = enc.encode('utf8')
    enc = base64.b64decode(enc)
    cipher = AES.new(self.key, AES.MODE_CBC, self.iv)
    decrypted = cipher.decrypt(enc)
    return self._unpad(decrypted.decode('utf8'))
class AESSkyPay:
  """
  Tested under Python 3.7 and pycryptodome
  """
  BLOCK_SIZE = 16
  def __init__(self, key):
    s1 = hashlib.sha1(bytes(key, encoding='utf-8')).digest()
    s2 = hashlib.sha1(s1).digest()
    self.key = s2[0:16]
    self.mode = AES.MODE_ECB
  def pkcs5_pad(self,s):
    BS = self.BLOCK_SIZE
    return s + ((BS - len(s) % BS) * chr(BS - len(s) % BS)).encode('utf8')
  def pkcs5_unpad(self,s):
    """
    unpadding according to PKCS #5
    @param s: string to unpad
    @type s: string
    @rtype: string
    """
    return s[:-ord(s[len(s) - 1:])]
  def encrypt(self, text):
    cryptor = AES.new(self.key, self.mode)
    # AES key must be either 16, 24, or 32 bytes long
    ciphertext = cryptor.encrypt(self.pkcs5_pad(text.encode('utf8')))
    return base64.b64encode(ciphertext).decode()
  def decrypt(self, text):
    cryptor = AES.new(self.key, self.mode)
    plain_text = cryptor.decrypt(base64.b64decode(text))
    return bytes.decode(self.pkcs5_unpad(plain_text))
def aes_decrypt(ciphertext, secret=None, prefix='aes:::'):
  secret = secret if secret else settings.default_aes_secret
  cipher = AESEncrypter(secret)
  prefix_len = len(prefix)
  if ciphertext[0:prefix_len]==prefix:
    return cipher.decrypt(ciphertext[prefix_len:])
  else:
    return ciphertext
def aes_encrypt(plaintext, secret=None, prefix='aes:::'):
  secret = secret if secret else settings.default_aes_secret
  cipher = AESEncrypter(secret)
  encrypted = cipher.encrypt(plaintext)
  return '%s%s' % (prefix, encrypted)



class Hardware:
    def get_cpu_sn():
        c = wmi.WMI()
        for cpu in c.Win32_Processor():
            return cpu.ProcessorId.strip()

    def get_disk_sn():
        """
        获取硬盘序列号
        """
        c = wmi.WMI()
        disk_sn_list = []
        for physical_disk in c.Win32_DiskDrive():
            disk_sn_list.append(physical_disk.SerialNumber.replace(" ", ""))
        return disk_sn_list


if __name__ == "__main__":
  try:
    # for AES test
    '''
    测试-初次运行时间加密
    '''
    dt = datetime.datetime.now()
    init = dt.strftime("%Y-%m-%d")
    print("加密前时间变量："+init)
    
    #用户密钥
    key = 'abc20304050607081q2w3e4r*1K|j!ta'
    
    cipher = AESEncrypter(key)
    encrypted = cipher.encrypt(init)
    print('Encrypted: %s' % encrypted)
    ciphertext = 'zgkxxMPkohD7eruHEQ744Q=='
    #check wether 2 strings are the same
    assert encrypted == ciphertext
    
    '''
    测试-读取用户电脑硬盘序列号并加密
    '''
    cpu = Hardware.get_cpu_sn()
    disk = Hardware.get_disk_sn()
    encrypted_cpu = cipher.encrypt(cpu)
    print(encrypted_cpu)
    plaintext2 = "DlE06C/szD9yIVDzD1lWXpkuII+AGJYTfJjjH2xjzAU="
    assert encrypted_cpu == plaintext2
    decrypted_cpu = cipher.decrypt(encrypted_cpu)
    print('解码后硬盘序列: %s' % decrypted_cpu)
    
    code_sample = "a = 5\nprint('小于10') if a<10 else print('大于10小于20') if a<20  else print('大于20小于30') if a< 30 else print('大于30')"
    encrypted_code = cipher.encrypt(code_sample)
    print(encrypted_code)
    decrypted_code = cipher.decrypt(encrypted_code)
    print('解码后code:\n', decrypted_code)
  except KeyboardInterrupt:
    sys.exit(0)