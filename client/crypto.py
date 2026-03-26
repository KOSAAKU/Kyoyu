import os 
import hashlib 
import base64 
from cryptography.fernet import Fernet 

def hash_uid(uid):
    h = hashlib.sha256() 
    h.update(uid.encode()) 
    return h.hexdigest() 

def generate_salt(): 
    return os.urandom(16) 

def derive_key(uid, salt): 
    key = hashlib.pbkdf2_hmac('sha256', uid.encode(), salt, 100000) 
    return base64.urlsafe_b64encode(key).decode('utf-8') 

def encrypt(message, key):
    return Fernet(key).encrypt(message.encode()).decode('utf-8') 

def decrypt(message, key):
    return Fernet(key).decrypt(message.encode()).decode('utf-8') 