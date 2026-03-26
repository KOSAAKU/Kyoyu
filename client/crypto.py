import os #os est utilisé pour générer un salt aléatoire de 16 octets avec os.urandom(16), qui est une fonction sécurisée pour la génération de données aléatoires cryptographiques.
import hashlib #hashlib est utilisé pour effectuer des opérations de hachage cryptographique, comme le calcul du hash SHA-256 d'un UID et la dérivation de clés à partir d'un UID et d'un salt en utilisant PBKDF2-HMAC-SHA256.
import base64 #base64 est utilisé pour encoder les clés dérivées en une chaîne de caractères lisible, compatible avec Fernet, qui nécessite des clés sous forme de chaînes base64 "URL-safe".
from cryptography.fernet import Fernet #Fernet est une bibliothèque de chiffrement symétrique qui fournit une interface simple pour chiffrer et déchiffrer des données de manière sécurisée, en utilisant AES en mode CBC avec un HMAC pour l'authentification.

def hash_uid(uid): #Calcule et retourne le hash SHA-256 d'un UID sous forme de chaîne hexadécimale pour vérification d'intégrité.
    h = hashlib.sha256() #Crée un objet SHA-256 vide pour le hachage 
    h.update(uid.encode()) #Ajoute l'UID à l'objet hash pour commencer le SHA-256.
    return h.hexdigest() #Retourne le hash SHA-256 final sous forme de chaîne hexadécimale lisible

def generate_salt(): 
    return os.urandom(16) #Génère un salt aléatoire de 16 octets

def derive_key(uid, salt): #Derive une clé de chiffrement à partir d'un UID et d'un salt en utilisant PBKDF2-HMAC-SHA256, avec 100000 itérations pour renforcer la sécurité contre les attaques par force brute.
    key = hashlib.pbkdf2_hmac('sha256', uid.encode(), salt, 100000) #transforme un UID faible en clé pratiquement incassable
    return base64.urlsafe_b64encode(key).decode('utf-8') #Transforme les bytes de la clé en une chaîne base64 "URL-safe" (sans +//) lisible par Fernet.

def encrypt(message, key):
    return Fernet(key).encrypt(message.encode()).decode('utf-8') #Chiffre un message en utilisant la clé dérivée, encode le message en bytes, chiffre avec Fernet, puis décode le résultat en UTF-8 pour une chaîne lisible.

def decrypt(message, key):
    return Fernet(key).decrypt(message.encode()).decode('utf-8') #Déchiffre un message chiffré en utilisant la clé dérivée, encode le message en bytes, déchiffre avec Fernet, puis décode le résultat en UTF-8 pour une chaîne lisible.