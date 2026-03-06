# RansomLab: Hybrid Cryptographic Simulation & Recovery Research
A high-fidelity simulation environment developed to demonstrate the mechanics of Hybrid Cryptography (AES-256 and RSA-2048). This project serves as a controlled laboratory for studying file system encryption, key management, and data recovery procedures in the context of modern cybersecurity threats.

## ⚠️ Ethical Use & Safety Disclaimer
This project is for educational and research purposes only. It is hardcoded to operate strictly within the Fish_Data/ sandbox to prevent accidental data loss. Unauthorized use of these techniques against systems without explicit permission is strictly prohibited.

### Technical Architecture
The lab utilizes a dual-layer encryption scheme, which is the industry standard for secure data transit and sophisticated encryption-based attacks:

Symmetric Layer (AES-256): Uses the cryptography.fernet module to perform high-speed encryption of individual file contents.

Asymmetric Layer (RSA-2048): Generates a session-specific AES key which is then "wrapped" (encrypted) using a Public RSA key. This ensures that the only way to recover files is with the corresponding Private RSA key.

Recursive Traversal: Implements os.walk to identify and process all files within the isolated target directory.

State Management: Automatically appends a .locked extension to encrypted files to prevent "Double Encryption" and track the simulation state.

### Project Components
gen_keys.py: Administrative script to generate the RSA Public/Private key pair.

encryptor.py: The simulation engine that traverses the sandbox, encrypts data, and renames files to .locked.

decryptor.py: The recovery utility that utilizes the Private Key to unlock the session key and restore original data.

Fish_Data/: The isolated directory used for all simulation activities.

### How to Run
Setup: Generate your keys by running python gen_keys.py.

Simulation: Place test files in Fish_Data/ and run python encryptor.py.

Recovery: Restore the files to their original state by running python decryptor.py.
