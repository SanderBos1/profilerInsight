
from flask_sqlalchemy import SQLAlchemy

class SingletonDB:
    """
    A singleton class that loads the database that is used by the flask application.

    Paramters:
        - N / A

    Example Usage:
        from module_name import SingletonDB

        db = SingletonDB.get_instance()
        # Now `db` can be used to interact with the database.

    """

    _instance = None

    @classmethod
    def get_instance(cls):
        """
        Get the singleton instance of SQLAlchemy.

        If the instance does not exist, it is created and initialized.

        Returns:
            SQLAlchemy: The singleton instance of SQLAlchemy.

        Example usage:

            >>> db = SingletonDB.get_instance()
            >>> type(db)
            <class 'flask_sqlalchemy.SQLAlchemy'>

        """
        if cls._instance is None:
            cls._instance = SQLAlchemy()
        return cls._instance
