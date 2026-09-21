import os
import sys
from cryptography.fernet import Fernet, InvalidToken


def generate_key():
    """Generate a new secret key and save it to a file."""
    key = Fernet.generate_key()
    key_filename = input("Enter filename to save the key (e.g., secret.key): ").strip()
    if not key_filename:
        key_filename = "secret.key"

    with open(key_filename, "wb") as key_file:
        key_file.write(key)

    print(f"\n[+] Secret key generated and saved to '{key_filename}'")
    print("[!] Keep this key safe. You need it to decrypt your files.\n")


def load_key(key_filename):
    """Load the secret key from a file."""
    try:
        with open(key_filename, "rb") as key_file:
            return key_file.read()
    except FileNotFoundError:
        print(f"[!] Key file '{key_filename}' not found.")
        return None


def encrypt_file():
    """Encrypt the contents of a file using the provided secret key."""
    file_path = input("Enter the path of the file to encrypt: ").strip()
    if not os.path.isfile(file_path):
        print("[!] File not found.")
        return

    key_filename = input("Enter the path of the secret key file: ").strip()
    key = load_key(key_filename)
    if key is None:
        return

    try:
        fernet = Fernet(key)
    except (ValueError, TypeError):
        print("[!] Invalid key.")
        return

    with open(file_path, "rb") as f:
        original_data = f.read()

    encrypted_data = fernet.encrypt(original_data)

    output_path = file_path + ".enc"
    with open(output_path, "wb") as f:
        f.write(encrypted_data)

    print(f"\n[+] File encrypted successfully -> '{output_path}'\n")


def decrypt_file():
    """Decrypt a previously encrypted file using the correct secret key."""
    file_path = input("Enter the path of the file to decrypt: ").strip()
    if not os.path.isfile(file_path):
        print("[!] File not found.")
        return

    key_filename = input("Enter the path of the secret key file: ").strip()
    key = load_key(key_filename)
    if key is None:
        return

    try:
        fernet = Fernet(key)
    except (ValueError, TypeError):
        print("[!] Invalid key.")
        return

    with open(file_path, "rb") as f:
        encrypted_data = f.read()

    try:
        decrypted_data = fernet.decrypt(encrypted_data)
    except InvalidToken:
        print("[!] Decryption failed. Incorrect key or corrupted/tampered file.")
        return

    if file_path.endswith(".enc"):
        output_path = file_path[:-4] + ".dec"
    else:
        output_path = file_path + ".dec"

    with open(output_path, "wb") as f:
        f.write(decrypted_data)

    print(f"\n[+] File decrypted successfully -> '{output_path}'\n")


def main_menu():
    while True:
        print("=" * 50)
        print("      FILE ENCRYPTION / DECRYPTION TOOL")
        print("=" * 50)
        print("1. Generate Secret Key")
        print("2. Encrypt a File")
        print("3. Decrypt a File")
        print("4. Exit")
        print("-" * 50)

        choice = input("Enter your choice (1-4): ").strip()
             
        if choice == "1":
            generate_key()
        elif choice == "2":
            encrypt_file()
        elif choice == "3":
            decrypt_file()
        elif choice == "4":
            print("Exiting... Goodbye!")
            sys.exit(0)
        else:
            print("[!] Invalid choice. Please select between 1 and 4.\n")


if __name__ == "__main__":
    main_menu()
