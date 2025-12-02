from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives import serialization 
from cryptography.hazmat.primitives.asymmetric import utils
import base64
import hashlib
import json
from time import time


class Transaction:
    def __init__(self, sender_address, recipient_address, amount):
        self.sender_address = sender_address  # Clave Pública del remitente
        self.recipient_address = recipient_address # Clave Pública del destinatario
        self.amount = amount
        self.timestamp = time.time()
        self.signature = None
    
    def to_string(self):
        """Genera un string de los datos de la transacción para ser hasheado y firmado."""
        return json.dumps({
            'sender': self.sender_address,
            'recipient': self.recipient_address,
            'amount': self.amount,
            'timestamp': self.timestamp
        }, sort_keys=True)

    def sign_transaction(self, wallet):
        """Firma la transacción usando el objeto Wallet del remitente."""
        # La firma se realiza sobre el hash de los datos (to_string)
        self.signature = wallet.sign(self.to_string())
    
    def is_valid(self):
        """Verifica si la transacción fue firmada por su supuesto remitente."""
        # Las transacciones de minería (sin remitente) se asumen válidas por simplicidad
        if self.sender_address == 'COINBASE':
            return True
        
        if not self.signature:
            return False # Debe estar firmada
        
        try:
            # 1. Reconstruir la Clave Pública del remitente
            pem_bytes = self.sender_address.encode('utf-8')
            public_key = serialization.load_pem_public_key(pem_bytes)
            
            # 2. Reconstruir la firma y el hash original
            signature_bytes = base64.b64decode(self.signature)
            hashed_data = hashlib.sha256(self.to_string().encode()).digest()

            # 3. Verificar la firma
            public_key.verify(
                signature_bytes,
                hashed_data,
                padding.PSS(
                    mgf=padding.MGF1(hashes.SHA256()),
                    salt_length=padding.PSS.MAX_LENGTH
                ),
                hashes.SHA256()
            )
            return True # Si la verificación no lanza excepción, es válida

        except Exception as e:
            # Si hay cualquier error (firma incorrecta, clave corrupta, etc.)
            return False