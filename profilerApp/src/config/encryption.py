"""
Module for managing a singleton instance of Fernet for encryption.
"""
import os
from cryptography.fernet import Fernet

# Singleton instance of Fernet cipher suite
_CIPHER_SUITE = None

def get_cipher_suite():
    """
    Get the singleton instance of Fernet cipher suite.

    If the instance does not exist, it is created and initialized using
    the ENCRYPTION_KEY environment variable.

    Returns:
        Fernet: The singleton instance of Fernet cipher suite.

    Raises:
        EnvironmentError: If the ENCRYPTION_KEY environment variable is not set.
    """
    global _CIPHER_SUITE
    if _CIPHER_SUITE is None:
        key = os.getenv('ENCRYPTION_KEY')
        if key is None:
            raise EnvironmentError("ENCRYPTION_KEY environment variable is not set")
        _CIPHER_SUITE = Fernet(key)
    return _CIPHER_SUITE
