#!/usr/bin/env python3
"""
cli.py - Interfaz de línea de comandos (CLI) para la blockchain.

Permite interactuar con la blockchain de forma manual:
- Crear wallets
- Crear transacciones
- Ver cadena
- Validar integridad

Uso: python cli.py
"""

import sys
sys.path.insert(0, 'src')

from Wallet import Wallet
from Transaction import Transaction
from Blockchain import Blockchain


def mostrar_menu():
    """Muestra el menú principal."""
    print("\n" + "=" * 50)
    print("  MENÚ BLOCKCHAIN")
    print("=" * 50)
    print("1. Crear nuevo wallet")
    print("2. Ver wallets creados")
    print("3. Crear transacción")
    print("4. Ver cadena de bloques")
    print("5. Validar cadena")
    print("6. Información de dificultad")
    print("7. Salir")
    print("=" * 50)


def main():
    """Función principal del CLI."""
    print("\n╔════════════════════════════════════╗")
    print("║  BIENVENIDO A LA BLOCKCHAIN       ║")
    print("╚════════════════════════════════════╝")
    
    # Inicializar blockchain
    print("\n¿Cuál es la dificultad de minería? (por defecto 3): ", end="")
    try:
        dificultad = int(input().strip() or "3")
    except ValueError:
        dificultad = 3
    
    blockchain = Blockchain(difficulty=dificultad)
    wallets = {}
    
    while True:
        mostrar_menu()
        opcion = input("\nElige opción (1-7): ").strip()
        
        if opcion == "1":
            # Crear nuevo wallet
            nombre = input("\n¿Nombre del wallet? (ej: Alice): ").strip()
            if nombre in wallets:
                print(f"✗ El wallet '{nombre}' ya existe")
            else:
                wallets[nombre] = Wallet()
                print(f"✓ Wallet '{nombre}' creado exitosamente")
        
        elif opcion == "2":
            # Ver wallets creados
            if wallets:
                print(f"\n📋 Wallets creados ({len(wallets)}):")
                for i, nombre in enumerate(wallets.keys(), 1):
                    print(f"  {i}. {nombre}")
            else:
                print("\n✗ No hay wallets creados aún")
        
        elif opcion == "3":
            # Crear transacción
            if len(wallets) < 2:
                print("\n✗ Necesitas al menos 2 wallets para hacer una transacción")
                print(f"   Wallets disponibles: {len(wallets)}")
            else:
                print(f"\nWallets disponibles: {list(wallets.keys())}")
                remitente = input("¿Remitente? ").strip()
                destinatario = input("¿Destinatario? ").strip()
                
                if remitente not in wallets or destinatario not in wallets:
                    print("✗ Wallets no válidos")
                elif remitente == destinatario:
                    print("✗ El remitente y destinatario no pueden ser iguales")
                else:
                    try:
                        monto = float(input("¿Monto? "))
                        if monto <= 0:
                            print("✗ El monto debe ser positivo")
                        else:
                            print("\n⛏️  Minando bloque...")
                            tx = Transaction(
                                wallets[remitente].get_public_key_pem(),
                                wallets[destinatario].get_public_key_pem(),
                                monto
                            )
                            tx.sign_transaction(wallets[remitente])
                            blockchain.add_block([tx.to_string()])
                            print(f"✓ Transacción de {monto} unidades de {remitente} -> {destinatario}")
                    except ValueError:
                        print("✗ Monto inválido")
        
        elif opcion == "4":
            # Ver cadena de bloques
            print(f"\n📦 Cadena de bloques ({len(blockchain.chain)} bloques):\n")
            for bloque in blockchain.chain:
                print(f"Bloque #{bloque.index}")
                print(f"  Hash: {bloque.hash}")
                print(f"  Nonce: {bloque.nonce}")
                print(f"  Transacciones: {len(bloque.transactions)}")
                print()
        
        elif opcion == "5":
            # Validar cadena
            print("\n🔍 Validando cadena...")
            if blockchain.is_chain_valid():
                print("✓ Cadena válida - integridad verificada")
            else:
                print("✗ Cadena inválida - se detectó corrupción")
        
        elif opcion == "6":
            # Información de dificultad
            print(f"\n📊 Información:")
            print(f"  Dificultad actual: {blockchain.difficulty}")
            print(f"  Bloques en cadena: {len(blockchain.chain)}")
            print(f"  Wallets creados: {len(wallets)}")
        
        elif opcion == "7":
            # Salir
            print("\n¡Hasta luego! 👋")
            break
        
        else:
            print("\n✗ Opción no válida (elige 1-7)")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n¡Programa interrumpido por el usuario!")
    except Exception as e:
        print(f"\n✗ Error: {e}")
