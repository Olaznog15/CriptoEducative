# Cripto_project

Implementación didáctica y minimalista de una blockchain con transacciones firmadas y minería por Prueba de Trabajo (PoW). El objetivo de este proyecto es servir como ejemplo y material de aprendizaje para entender los componentes básicos de una blockchain: bloques, minería, transacciones firmadas y validación de la cadena.

---

## 📚 Visión general

- Bloques con PoW (dificultad configurable: número de ceros iniciales).
- Transacciones firmadas con RSA (PSS + SHA-256).
- Wallets que generan par de claves RSA y firman transacciones.
- Validación de integridad de cadena: hash por bloque, enlace anterior y comprobación de PoW.
- Bloque Génesis creado automáticamente al iniciar la cadena.

---

## 🧭 Estructura del proyecto

- `Wallet.py` — Generación de clave RSA, exportación de clave pública en formato PEM y firma de mensajes.
- `Transaction.py` — Representa una transacción (sender, recipient, amount, timestamp, signature). Permite serializar, firmar y verificar la firma.
- `Block.py` — Define la estructura del bloque y contiene los métodos `calculate_hash()` y `mine_block(difficulty)` (PoW simple).
- `Blockchain.py` — Mantiene una lista de bloques, crea el bloque génesis, añade bloques y valida la cadena con `is_chain_valid()`.

---

## ⚙️ Requisitos

- Python 3.8+
- Paquetes: `cryptography`

Se recomienda crear un entorno virtual antes de instalar dependencias:

```bash
python -m venv .venv
source .venv/bin/activate
pip install cryptography
```

---

## 🚀 Uso básico (ejemplo)

```python
from Wallet import Wallet
from Transaction import Transaction
from Blockchain import Blockchain

# Crear wallets
wallet_a = Wallet()
wallet_b = Wallet()

# Crear y firmar transacción
tx = Transaction(wallet_a.get_public_key_pem(), wallet_b.get_public_key_pem(), 10)
tx.sign_transaction(wallet_a)

# Crear blockchain y añadir bloque con la transacción
chain = Blockchain(difficulty=3)
chain.add_block([tx.to_string()])

print("¿Cadena válida?", chain.is_chain_valid())
```

El ejemplo anterior muestra el flujo básico: crear wallets, firmar una transacción, minar un bloque con PoW y validar la cadena.

---

## 🧩 Diseño y notas de implementación

1. Wallet
   - Genera un par de claves RSA (privada/pública).
   - `get_public_key_pem()` devuelve la clave pública en PEM (se usa como "dirección").
   - `sign(message)` firma el hash SHA-256 del mensaje y devuelve la firma en Base64.

2. Transaction
   - Contiene `sender_address`, `recipient_address`, `amount`, `timestamp` y `signature`.
   - `to_string()` serializa la transacción (ordenada por claves) para hashear y firmar.
   - `sign_transaction(wallet)` usa la instancia `Wallet` del remitente para firmar.
   - `is_valid()` reconstruye la clave pública desde el PEM y verifica la firma con PSS+SHA256.

3. Block
   - Atributos: `index`, `timestamp`, `transactions`, `previous_hash`, `nonce`, `hash`.
   - `calculate_hash()` calcula SHA-256 del bloque (incluyendo nonce y timestamp).
   - `mine_block(difficulty)` incrementa nonce hasta encontrar un hash con `difficulty` ceros al inicio.

4. Blockchain
   - `chain` es una lista de bloques; `difficulty` controla el trabajo de minería.
   - `create_genesis_block()` crea el primer bloque manualmente.
   - `add_block(transactions)` crea-mina y añade un bloque nuevo.
   - `is_chain_valid()` valida la integridad de la cadena: hash actual, enlace a bloque previo y PoW.

---

## ⚠️ Limitaciones importantes

- Proyecto didáctico, NO apto para producción.
- No hay red P2P, ni consenso distribuido ni persistencia avanzada.
- No se gestiona un libro de cuentas robusto (UTXO o saldos por cuenta) — esto es sólo una demostración.
- Uso de RSA para firmas y PoW simple sólo con fines educativos (implementaciones reales usan ECDSA/Ed25519, redes, consenso, y mecanismos robustos).

---

## ✅ Posibles mejoras y próximos pasos

- Añadir tests unitarios automatizados.
- Implementar manejo de saldos (UTXO o modelo de cuentas) y checks de saldo antes de permitir transacciones.
- Añadir persistencia en disco para la cadena y las transacciones.
- Reemplazar RSA por ECDSA / Ed25519 para firmas más realistas.
- Crear un CLI o API (Flask/FastAPI) para interactuar con la cadena.

---

## 📬 Contribuciones y licencia

La idea del proyecto es puramente didactica, no tengo intencion de mantener ni ampliar el proyecto. Pudes usar la informacion de este proyecto como mejor consideres.