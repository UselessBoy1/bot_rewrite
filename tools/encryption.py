from cryptography.fernet import Fernet
import os

key = os.environ['KEY'].encode("ASCII")

f = Fernet(key)

def encrypt(text :str):
    return f.encrypt(text.encode("UTF-8"))

def decrypt(crypt :bytes):
    return f.decrypt(crypt).decode("UTF-8")
