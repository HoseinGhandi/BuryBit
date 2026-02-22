# 🕳️ BuryBit
> *"If you want to hide a secret, put it in plain sight."*

**BuryBit** is a high-entropy, polymorphic steganography engine engineered for Red Team operators, privacy absolutists, and anti-forensics scenarios. It goes beyond traditional encryption by deploying psychological warfare tactics and plausible deniability against advanced forensic analysis.

## ⚠️ Status: Active Development (V1.0 Blueprint)
This repository is currently under heavy reconstruction. We are transitioning from a successful proof-of-concept to a military-grade, zero-trust architecture. Every line of code is being rewritten with absolute paranoia.

## 🧠 Core Pillars (The Paranoia Protocol)

BuryBit is built upon three uncompromising architectural concepts:

### 1. The Argon Nexus (Memory-Hard Cryptography)
Traditional brute-force attacks rely on GPU/ASIC farms. BuryBit neutralizes this hardware advantage by utilizing **Argon2id**. By artificially inflating the RAM requirements for every single password derivation (e.g., forcing 512MB of active memory per guess), we shift the battleground from processing power to physical silicon limitations, rendering global-scale brute-forcing economically and physically unfeasible.

### 2. Plausible Deniability (The Decoy Vault)
If subjected to coercive interrogation (the "5-dollar wrench attack"), standard encryption fails. BuryBit employs a multi-vault structure. Providing a secondary "Decoy Password" silently unlocks an authentic-looking fake vault (e.g., harmless family photos or university PDFs). There is mathematically zero evidence left behind to prove the existence of the primary hidden payload.

### 3. Scorched Earth (The Cyanide Protocol)
A targeted counter-measure for extreme scenarios. If an operator is forced to provide the ultimate access key, they can input the "Cyanide Password". Instead of unlocking the data, the engine silently executes an in-memory burn protocol (`VirtualAlloc`/`RtlMoveMemory`), surgically overwriting the hidden payload with absolute noise. The carrier file remains fully intact, presenting a plausible `[WinError 23] Cyclic Redundancy Check` to forensic analysts, permanently destroying the payload while protecting the operator.

## 🏗️ Architecture & Stack
* **Core Engine:** Python 3 (Rapid logic execution & file IO)
* **Memory Management:** C/Shellcode Injection (For zero-footprint memory wiping)
* **Cryptography:** Argon2id + XOR Stream Ciphers

## ⚖️ License
This project is open-sourced under the **Apache License 2.0**. 
Built for the shadows. Engineered for survival.