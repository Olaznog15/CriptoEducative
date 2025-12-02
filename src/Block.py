import hashlib
import json
import time

class Block:
    def __init__(self, index, transactions, previous_hash, difficulty):
        self.index = index
        self.timestamp = time.time()
        self.transactions = transactions
        self.previous_hash = previous_hash
        self.nonce = 0
        self.hash = self.calculate_hash()
        self.mine_block(difficulty)

    def calculate_hash(self):
        """Calcula el hash SHA-256 del bloque."""
        # Concatenamos todos los atributos clave en un string.
        # Es crucial incluir el nonce, ya que es lo que cambia durante la minería.
        block_string = json.dumps({
            'index': self.index,
            'timestamp': self.timestamp,
            'transactions': self.transactions,
            'previous_hash': self.previous_hash,
            'nonce': self.nonce
        }, sort_keys=True).encode()
        
        return hashlib.sha256(block_string).hexdigest()

    def mine_block(self, difficulty):
        """Implementa el algoritmo de Prueba de Trabajo (PoW)."""
        # El objetivo (target) es una cadena de '0's de longitud 'difficulty'.
        target = "0" * difficulty  
        
        print(f"\n Comenzando minería del Bloque #{self.index}...")
        
        # Iteramos (incrementando el nonce) hasta que el hash satisfaga el objetivo.
        while self.hash[:difficulty] != target:
            self.nonce += 1
            self.hash = self.calculate_hash()

        print(f" Bloque minado con éxito!")
        print(f"   Hash: {self.hash}")
        print(f"   Nonce: {self.nonce}")