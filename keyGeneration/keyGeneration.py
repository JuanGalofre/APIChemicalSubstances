from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from base64 import urlsafe_b64encode, urlsafe_b64decode

def generate_aes_key(password, salt):
    # Derive a 256-bit key using PBKDF2-HMAC-SHA256
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        salt=salt,
        iterations=100000,  # Adjust the number of iterations based on your security requirements
        length=32  # 32 bytes (256 bits) key size for AES-256
    )

    key = kdf.derive(password.encode())
    return key

# Example usage with a random salt
import os

password = "secret_password_for_hashing"
salt = os.urandom(16)  # Generate a random 16-byte salt

secret_key = generate_aes_key(password, salt)
print(f"Generated AES secret key: {urlsafe_b64encode(secret_key).decode()}")
print(f"Salt: {urlsafe_b64encode(salt).decode()}")
