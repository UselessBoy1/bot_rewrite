import os

from cryptography.fernet import Fernet
from hashlib import sha256

key = os.environ['KEY'].encode("ASCII")
f = Fernet(key)

def encrypt(text :str):
    return f.encrypt(text.encode("UTF-8"))

def decrypt(crypt :bytes):
    return f.decrypt(crypt).decode("UTF-8")

def is_web_pwd_ok(pwd):
    return sha256(pwd.encode('UTF-8')).hexdigest() != "4e61a50731ffc4c2b7519708b556de4d0ff7a988a441d78c077b6d7b20b82cc7"
