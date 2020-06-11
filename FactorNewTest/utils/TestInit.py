#coding:utf-8
import base64
from pyDes import _baseDes, PAD_NORMAL, ECB, CBC, des, _pythonMajorVersion, PAD_PKCS5
class triple_des(_baseDes):
  """Triple DES encryption/decrytpion class
  This algorithm uses the DES-EDE3 (when a 24 byte key is supplied) or
  the DES-EDE2 (when a 16 byte key is supplied) encryption methods.
  Supports ECB (Electronic Code Book) and CBC (Cypher Block Chaining) modes.
  pyDes.des(key, [mode], [IV])
  key -> Bytes containing the encryption key, must be either 16 or
 bytes long
  mode -> Optional argument for encryption type, can be either pyDes.ECB
    (Electronic Code Book), pyDes.CBC (Cypher Block Chaining)
  IV  -> Optional Initial Value bytes, must be supplied if using CBC mode.
    Must be 8 bytes in length.
  pad -> Optional argument, set the pad character (PAD_NORMAL) to use
    during all encrypt/decrpt operations done with this instance.
  padmode -> Optional argument, set the padding mode (PAD_NORMAL or
    PAD_PKCS5) to use during all encrypt/decrpt operations done
    with this instance.
  """
  def __init__(self, key, mode=ECB, IV=None, pad=None, padmode=PAD_NORMAL):
    _baseDes.__init__(self, mode, IV, pad, padmode)
    self.setKey(key)
  def setKey(self, key):
    """Will set the crypting key for this object. Either 16 or 24 bytes long."""
    self.key_size = 24 # Use DES-EDE3 mode
    if len(key) != self.key_size:
      if len(key) == 16: # Use DES-EDE2 mode
        self.key_size = 16
      else:
        raise ValueError("Invalid triple DES key size. Key must be either 16 or 24 bytes long")
    if self.getMode() == CBC:
      if not self.getIV():
        # Use the first 8 bytes of the key
        self._iv = key[:self.block_size]
      if len(self.getIV()) != self.block_size:
        raise ValueError("Invalid IV, must be 8 bytes in length")
    self.__key1 = des(key[:8], self._mode, self._iv,
         self._padding, self._padmode)
    self.__key2 = des(key[8:16], self._mode, self._iv,
         self._padding, self._padmode)
    if self.key_size == 16:
      self.__key3 = self.__key1
    else:
      self.__key3 = des(key[16:], self._mode, self._iv,
           self._padding, self._padmode)
    _baseDes.setKey(self, key)
  # Override setter methods to work on all 3 keys.
  def setMode(self, mode):
    """Sets the type of crypting mode, pyDes.ECB or pyDes.CBC"""
    _baseDes.setMode(self, mode)
    for key in (self.__key1, self.__key2, self.__key3):
      key.setMode(mode)
  def setPadding(self, pad):
    """setPadding() -> bytes of length 1. Padding character."""
    _baseDes.setPadding(self, pad)
    for key in (self.__key1, self.__key2, self.__key3):
      key.setPadding(pad)
  def setPadMode(self, mode):
    """Sets the type of padding mode, pyDes.PAD_NORMAL or pyDes.PAD_PKCS5"""
    _baseDes.setPadMode(self, mode)
    for key in (self.__key1, self.__key2, self.__key3):
      key.setPadMode(mode)
  def setIV(self, IV):
    """Will set the Initial Value, used in conjunction with CBC mode"""
    _baseDes.setIV(self, IV)
    for key in (self.__key1, self.__key2, self.__key3):
      key.setIV(IV)
  def encrypt(self, data, pad=None, padmode=None):
    """encrypt(data, [pad], [padmode]) -> bytes
    data : bytes to be encrypted
    pad : Optional argument for encryption padding. Must only be one byte
    padmode : Optional argument for overriding the padding mode.
    The data must be a multiple of 8 bytes and will be encrypted
    with the already specified key. Data does not have to be a
    multiple of 8 bytes if the padding character is supplied, or
    the padmode is set to PAD_PKCS5, as bytes will then added to
    ensure the be padded data is a multiple of 8 bytes.
    """
    ENCRYPT = des.ENCRYPT
    DECRYPT = des.DECRYPT
    data = self._guardAgainstUnicode(data)
    if pad is not None:
      pad = self._guardAgainstUnicode(pad)
    # Pad the data accordingly.
    data = self._padData(data, pad, padmode)
    if self.getMode() == CBC:
      self.__key1.setIV(self.getIV())
      self.__key2.setIV(self.getIV())
      self.__key3.setIV(self.getIV())
      i = 0
      result = []
      while i < len(data):
        block = self.__key1.crypt(data[i:i+8], ENCRYPT)
        block = self.__key2.crypt(block, DECRYPT)
        block = self.__key3.crypt(block, ENCRYPT)
        self.__key1.setIV(block)
        self.__key2.setIV(block)
        self.__key3.setIV(block)
        result.append(block)
        i += 8
      if _pythonMajorVersion < 3:
        return ''.join(result)
      else:
        return bytes.fromhex('').join(result)
    else:
      data = self.__key1.crypt(data, ENCRYPT)
      data = self.__key2.crypt(data, DECRYPT)
      return self.__key3.crypt(data, ENCRYPT)
  def decrypt(self, data, pad=None, padmode=None):
    """decrypt(data, [pad], [padmode]) -> bytes
    data : bytes to be encrypted
    pad : Optional argument for decryption padding. Must only be one byte
    padmode : Optional argument for overriding the padding mode.
    The data must be a multiple of 8 bytes and will be decrypted
    with the already specified key. In PAD_NORMAL mode, if the
    optional padding character is supplied, then the un-encrypted
    data will have the padding characters removed from the end of
    the bytes. This pad removal only occurs on the last 8 bytes of
    the data (last data block). In PAD_PKCS5 mode, the special
    padding end markers will be removed from the data after
    decrypting, no pad character is required for PAD_PKCS5.
    """
    ENCRYPT = des.ENCRYPT
    DECRYPT = des.DECRYPT
    data = self._guardAgainstUnicode(data)
    if pad is not None:
      pad = self._guardAgainstUnicode(pad)
    if self.getMode() == CBC:
      self.__key1.setIV(self.getIV())
      self.__key2.setIV(self.getIV())
      self.__key3.setIV(self.getIV())
      i = 0
      result = []
      while i < len(data):
        iv = data[i:i+8]
        block = self.__key3.crypt(iv,  DECRYPT)
        block = self.__key2.crypt(block, ENCRYPT)
        block = self.__key1.crypt(block, DECRYPT)
        self.__key1.setIV(iv)
        self.__key2.setIV(iv)
        self.__key3.setIV(iv)
        result.append(block)
        i += 8
      if _pythonMajorVersion < 3:
        data = ''.join(result)
      else:
        data = bytes.fromhex('').join(result)
    else:
      data = self.__key3.crypt(data, DECRYPT)
      data = self.__key2.crypt(data, ENCRYPT)
      data = self.__key1.crypt(data, DECRYPT)
    return self._unpadData(data, pad, padmode)


def factor_encrypt_identity(identity):
    if isinstance(identity,long):
        identity=str(identity)
    if isinstance(identity, int):
      identity = str(identity)
    identity=str(identity)
    key = "cf410f84904a44cc8a7f48fc4134e8f9"
    key = key[0:24]
    k = triple_des(key, ECB, IV=None, pad=None, padmode=PAD_PKCS5)
    encrypt_identity = k.encrypt(identity, padmode=PAD_PKCS5)
    return base64.b64encode(encrypt_identity)

def factor_decrypt_identity(identitySecret):
    key = "cf410f84904a44cc8a7f48fc4134e8f9"
    key = key[0:24]
    k = triple_des(key, ECB, IV=None, pad=None, padmode=PAD_PKCS5)
    decrypt_identity = k.decrypt(base64.b64decode(identitySecret), padmode=PAD_PKCS5)
    return decrypt_identity

if __name__=="__main__":
    key = "cf410f84904a44cc8a7f48fc4134e8f9"
    # key = "3b278cac3c23c9f9e69983df249e3caf"
    key=key[0:24]
    # print factor_encrypt_identity('倪英')
    # print factor_encrypt_identity('13917247121')
    # print factor_encrypt_identity('13436549943')

    # print factor_encrypt_identity('530181199304161830')
    # print factor_encrypt_identity('13924888245')

    print factor_decrypt_identity('C8wp3bQ64EUkl8OQrHq5wCsomicNGUqK')
    # print factor_decrypt_identity('OrIYBl3gbH9iXQt1Wu6kEQ==')