#!/usr/bin/env python3
"""
main.py - Script de demostración de la blockchain.

Ejecuta automáticamente una serie de operaciones:
- Crea dos wallets
- Realiza transacciones firmadas
- Mina bloques
- Valida la cadena

Uso: python main.py
"""

import sys
sys.path.insert(0, 'src')

from Wallet import Wallet
from Transaction import Transaction
from Blockchain import Blockchain


def main():
    print("=" * 50)
    print("  BLOCKCHAIN EN MARCHA")
    print("=" * 50)
    
    # Crear blockchain con dificultad 3
    print("\n[1/5] Inicializando blockchain (dificultad=3)...")
    blockchain = Blockchain(difficulty=3)
    
    # Crear dos wallets
    print("\n[2/5] Creando wallets...")
    wallet_a = Wallet()
    wallet_b = Wallet()
    print("✓ Wallet A creado")
    print("✓ Wallet B creado")
    
    # Primera transacción
    print("\n[3/5] Creando primera transacción (A -> B: 50 unidades)...")
    tx1 = Transaction(wallet_a.get_public_key_pem(), wallet_b.get_public_key_pem(), 50)
    tx1.sign_transaction(wallet_a)
    print("✓ Transacción creada y firmada")
    print("✓ Minando bloque...")
    blockchain.add_block([tx1.to_string()])
    
    # Segunda transacción
    print("\n[4/5] Creando segunda transacción (B -> A: 25 unidades)...")
    tx2 = Transaction(wallet_b.get_public_key_pem(), wallet_a.get_public_key_pem(), 25)
    tx2.sign_transaction(wallet_b)
    print("✓ Transacción creada y firmada")
    print("✓ Minando bloque...")
    blockchain.add_block([tx2.to_string()])
    
    # Validar la cadena
    print("\n[5/5] Validando integridad de la cadena...")
    if blockchain.is_chain_valid():
        print("✓ Cadena válida - todas las firmas y hashes verificados")
    else:
        print("✗ Cadena corrupta")
    
    # Resumen final
    print("\n" + "=" * 50)
    print("  RESUMEN FINAL")
    print("=" * 50)
    print(f"Total de bloques: {len(blockchain.chain)}")
    print(f"  - Bloque Génesis")
    for i in range(1, len(blockchain.chain)):
        print(f"  - Bloque #{i} (transacción #{i})")
    print("\nBlockchain operacional y validado ✓")
    print("=" * 50)


if __name__ == "__main__":
    main()
