
import os

from cryptography.fernet import Fernet

class SingletonFernet:
    """
    A Class for managing a singleton instance of Fernet for encryption.

    Example usage:

        from module_name import SingletonFernet

        cipher_suite = SingletonFernet.get_instance()
        encrypted_data = cipher_suite.encrypt(b'some data')
    """
    
    _instance = None

    @classmethod
    def get_instance(cls):
        """
        Get the singleton instance of the Fernet cipher suite.

        If the instance does not exist, it is created and initialized using
        the ENCRYPTION_KEY environment variable.

        Returns:
            Fernet: The singleton instance of Fernet cipher suite.

        Raises:
            EnvironmentError: If the ENCRYPTION_KEY environment variable is not set.

        Example usage:

            >>> cipher_suite = SingletonFernet.get_instance()
            >>> encrypted_data = cipher_suite.encrypt(b'some data')
            >>> decrypted_data = cipher_suite.decrypt(encrypted_data)
            >>> print(decrypted_data)
            b'some data'
        """
        if cls._instance is None:
            key = os.getenv('ENCRYPTION_KEY')
            if key is None:
                raise EnvironmentError("ENCRYPTION_KEY environment variable is not set")
            cls._instance = Fernet(key)
        return cls._instance
