from cryptography.fernet import Fernet
from hashlib import pbkdf2_hmac
from pathlib import Path
from base64 import urlsafe_b64encode

class Manager:
    def __init__(self, storage_path: str, key_path: str):
        self.f = None
        self.key = None
        self.encrypted_data = None
        self.decrypted_data = None
        self.data_lines = None
        self.password = None
        self.salt = None
        self.storage_path = storage_path
        self.key_path = key_path

    def genKey(self, password: str, salt: str):
        if self.keyFileExists():
            raise FileExistsError("The key file already exits, replacing it will cause loss of data. Key generation has been aborted.")
        else:
            password_enc = urlsafe_b64encode(password.encode())                                     # password_encoded
            salt_enc = urlsafe_b64encode(salt.encode())                                             # salt_encoded
            dec_k = urlsafe_b64encode(pbkdf2_hmac('sha256', password_enc, salt_enc, 100000))        # decryption_key
            encr_key = Fernet.generate_key()                                                        # encrypting_key
            key_encryptor = Fernet(dec_k)                                                           # key_encryptor
            key_encr = key_encryptor.encrypt(encr_key).decode("utf-8")                              # key_encrypted
            with open(self.key_path, "w") as file:
                file.write(key_encr)
    
    def setInstancePassword(self, password: str):
        self.password = urlsafe_b64encode(password.encode())
    
    def setInstanceSalt(self, salt: str):
        self.salt = urlsafe_b64encode(salt.encode())

    def readKey(self):
        with open(self.key_path, "r") as file:
            if self.password == None: raise RuntimeError("Password is not set.")
            if self.salt == None: raise RuntimeError("Salt is not set.")
            encr_key_key = urlsafe_b64encode(pbkdf2_hmac("sha256", self.password, self.salt, 100000))
            key_decryptor = Fernet(encr_key_key)
            key_encr = file.read()
            encr_key = key_decryptor.decrypt(key_encr.encode()).decode("utf-8")
            self.key = encr_key
            self.f = Fernet(self.key)

    def keyFileExists(self):
        file_path = Path(self.key_path)
        return file_path.is_file()

    def storageFileExists(self):
        file_path = Path(self.storage_path)
        return file_path.is_file()
    
    def storeData(self, value: str, index: int):
        if self.encrypted_data == None: self.refreshData()
        if index > self.data_lines: raise IndexError("Write index greater than last line.")

        value_enc = value.encode()
        encr_value = self.f.encrypt(value_enc)
        encr_value_dec = encr_value.decode("utf-8")

        if index == self.data_lines: 
            self.encrypted_data.append(encr_value_dec + "\n")
            self.decrypted_data.append(value)
            self.data_lines += 1
        else: 
            self.encrypted_data[index] = encr_value_dec + "\n"
            self.decrypted_data[index] = value

        with open(self.storage_path, "w") as file:
            file.writelines(self.encrypted_data)

    def refreshData(self):
        if not self.storageFileExists():
            # raise FileNotFoundError("Storage file not found")
            with open(self.storage_path, "w") as file:
                pass
        with open(self.storage_path, "r") as file:
            self.encrypted_data = file.readlines()
            self.data_lines = len(self.encrypted_data)
            self.decrypted_data = [None] * self.data_lines

    def decryptData(self):
        if self.key == None: self.readKey()
        if self.encrypted_data == None: self.refreshData()
        for i in range(self.data_lines):
            self.decrypted_data[i] = self.f.decrypt(self.encrypted_data[i].encode()).decode()
    
    def changePassword(self, newPassword, newSalt):
        if self.key == None:
            self.readKey()
        newPassword_enc = urlsafe_b64encode(newPassword.encode())
        newSalt_enc = urlsafe_b64encode(newSalt.encode())
        newKey_encryptor_key = urlsafe_b64encode(pbkdf2_hmac("sha256", newPassword_enc, newSalt_enc, 100000))
        newKey_encryptor = Fernet(newKey_encryptor_key)
        encr_newKey = newKey_encryptor.encrypt(self.key.encode()).decode()
        with open(self.key_path, "w") as file:
            file.write(encr_newKey)
        self.setInstancePassword(newPassword)
        self.setInstanceSalt(newSalt)