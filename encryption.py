"""
Module providing encrypting and decrypting of files using a key.
More importantly a way to define random states that persists for projects
"""

from random import randint, seed
from dataclasses import dataclass, field
from cryptography.fernet import Fernet

def decrypt(file, key_string, encoding = 'utf8'):
    """Decrypt a file using Fernet decryption

    Args:
        file (_type_): File Path that is to be decrypted
        key_string (_type_): Key used by Fernet
        encoding (str, optional): Encoding type of the file. Defaults to 'utf8'.

    Returns:
        Any: Decrypted contents of the file
    """
    key = bytes(key_string, encoding)
    cipher = Fernet(key)
    with open(file, "rb") as file:
        data = file.read()
        return cipher.decrypt(data)

def encrypt(file, key_string, encoding = 'utf8'):
    """Encrypt a file using Fernet decryption

    Args:
        file (_type_): File Path that is to be encrypted
        key_string (_type_): Key used by Fernet
        encoding (str, optional): Encoding type of the file. Defaults to 'utf8'.
    """
    key = bytes(key_string, encoding)
    cipher = Fernet(key)
    with open(file, "rb") as read_file:
        data = read_file.read()
        encrypted_data = cipher.encrypt(data)
    with open(file, "wb") as write_file:
        write_file.write(encrypted_data)

@dataclass
class RandomState():
    """_summary_
    Parameters
    ----------
    file : String
        File Path that is to be encrypted
    key_string : String
        String of the key used by Fernet
    encoding : String
        Encoding type of the file, default is utf8
    """
    seed : str
    state: int = field(init=False)

    def __post_init__(self):
        seed(self.seed)
        self.state = randint(1, 2**9)
