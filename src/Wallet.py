import hashlib
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import utils
import base64

class Wallet:
    def __init__(self):
        # Generar un par de claves RSA (comúnmente usado para demostración)
        self.private_key = rsa.generate_private_key(
            public_exponent=65537,
            key_size=2048
        )
        self.public_key = self.private_key.public_key()
    
    def get_public_key_pem(self):
        """Retorna la clave pública en formato PEM (fácil de compartir/usar como 'dirección')."""
        pem = self.public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        )
        # La dirección será una versión limpia y codificada de la clave pública
        return pem.decode('utf-8')

    def sign(self, message):
        """Firma un mensaje (hash de la transacción) con la clave privada."""
        # Se firma el hash del mensaje, no el mensaje completo
        hashed_data = hashlib.sha256(message.encode()).digest()
        
        signature = self.private_key.sign(
            hashed_data,
            padding.PSS(
                mgf=padding.MGF1(hashes.SHA256()),
                salt_length=padding.PSS.MAX_LENGTH
            ),
            hashes.SHA256()
        )
        # Codificamos la firma a Base64 para que sea transportable como string
        return base64.b64encode(signature).decode('utf-8')