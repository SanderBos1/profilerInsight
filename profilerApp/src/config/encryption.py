from cryptography.fernet import Fernet
import os

class EncryptionUtil:
    _cipher_suite = None

    @staticmethod
    def get_cipher_suite():
        if EncryptionUtil._cipher_suite is None:
            key = os.getenv('ENCRYPTION_KEY')
            if key is None:
                raise EnvironmentError("ENCRYPTION_KEY environment variable is not set")
            EncryptionUtil._cipher_suite = Fernet(key)
        return EncryptionUtil._cipher_suite

