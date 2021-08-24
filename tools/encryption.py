import os

from cryptography.fernet import Fernet

key = os.environ['KEY'].encode("ASCII")

f = Fernet(key)

def encrypt(text :str):
    return f.encrypt(text.encode("UTF-8"))

def decrypt(crypt :bytes):
    return f.decrypt(crypt).decode("UTF-8")
