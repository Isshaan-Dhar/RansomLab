import os
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import padding

def decrypt_lab():
    target_dir = "Fish_Data"
    key_path = os.path.join(target_dir, "DECRYPT_KEY.bin")

    if not os.path.exists("private.pem"):
        print("[-] Error: private.pem not found. Recovery impossible.")
        return
    if not os.path.exists(key_path):
        print("[-] Error: DECRYPT_KEY.bin not found in Fish_Data.")
        return

    with open("private.pem", "rb") as f:
        private_key = serialization.load_pem_private_key(f.read(), password=None)

    with open(key_path, "rb") as f:
        encrypted_session_key = f.read()
    
    try:
        session_key = private_key.decrypt(
            encrypted_session_key,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()), 
                algorithm=hashes.SHA256(), 
                label=None
            )
        )
        fernet = Fernet(session_key)
    except Exception as e:
        print(f"[-] Decryption Error (Invalid Key): {e}")
        return

    for root, dirs, files in os.walk(target_dir):
        for file in files:
            # Only process files with the .locked extension
            if not file.endswith(".locked"):
                continue
            
            file_path = os.path.join(root, file)
            
            with open(file_path, "rb") as f:
                encrypted_data = f.read()
            
            try:
                decrypted_data = fernet.decrypt(encrypted_data)
                
                original_path = file_path.replace(".locked", "")
                
                with open(original_path, "wb") as f:
                    f.write(decrypted_data)
                
                os.remove(file_path)
                print(f"[*] Restored: {file} -> {os.path.basename(original_path)}")
            except Exception as e:
                print(f"[-] Failed to decrypt {file}: {e}")

    os.remove(key_path)
    print("\n[+] Recovery Complete. All files restored.")

if __name__ == "__main__":

    decrypt_lab()
