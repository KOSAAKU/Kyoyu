import os
import hashlib
import base64
from cryptography.fernet import Fernet

def hash_uid(uid): #Calcule et retourne le hash SHA-256 d'un UID sous forme de chaîne hexadécimale pour vérification d'intégrité.
    h = hashlib.sha256() #Crée un objet SHA-256 vide pour le hachage 
    h.update(uid.encode()) #Ajoute l'UID à l'objet hash pour commencer le SHA-256.
    return h.hexdigest() #Retourne le hash SHA-256 final sous forme de chaîne hexadécimale lisible

def generate_salt():
    return os.urandom(16) #Génère un salt aléatoire de 16 octets

def derive_key(uid, salt):
    key = hashlib.pbkdf2_hmac('sha256', uid.encode(), salt, 100000) #transforme un UID faible en clé pratiquement incassable
    return base64.urlsafe_b64encode(key).decode('utf-8') #Transforme les bytes de la clé en une chaîne base64 "URL-safe" (sans +//) lisible par Fernet.

def encrypt(message, key):

def decrypt(message, key):