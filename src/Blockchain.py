from Block import Block


class Blockchain:
    def __init__(self, difficulty=4):
        self.chain = []
        self.difficulty = difficulty
        # El Bloque Génesis es el primer bloque, creado manualmente
        self.create_genesis_block()

    def create_genesis_block(self):
        """Crea el primer bloque de la cadena."""
        # El bloque génesis tiene un índice de 0 y un 'previous_hash' nulo.
        genesis_block = Block(0, ["Bloque Génesis"], "0", self.difficulty)
        self.chain.append(genesis_block)
        print("Blockchain inicializada con el Bloque Génesis.")

    @property
    def get_last_block(self):
        """Devuelve el último bloque de la cadena."""
        return self.chain[-1]

    def add_block(self, transactions):
        """Añade un nuevo bloque a la cadena."""
        latest_block = self.get_last_block
        new_index = latest_block.index + 1
        new_previous_hash = latest_block.hash
        
        # Creamos y minamos el nuevo bloque
        new_block = Block(new_index, transactions, new_previous_hash, self.difficulty)
        self.chain.append(new_block)

    def is_chain_valid(self):
        """Verifica la integridad de la cadena."""
        for i in range(1, len(self.chain)):
            current_block = self.chain[i]
            previous_block = self.chain[i-1]

            # 1. Verifica si el hash actual del bloque es correcto
            if current_block.hash != current_block.calculate_hash():
                print(f"Validación Fallida: Hash del Bloque #{current_block.index} es incorrecto.")
                return False

            # 2. Verifica si el enlace al bloque anterior es correcto
            if current_block.previous_hash != previous_block.hash:
                print(f"Validación Fallida: Enlace de hash roto en Bloque #{current_block.index}.")
                return False

            # 3. Verifica el PoW (si el hash cumple con la dificultad)
            target = "0" * self.difficulty
            if current_block.hash[:self.difficulty] != target:
                 print(f"Validación Fallida: PoW inválido en Bloque #{current_block.index}.")
                 return False

        return True