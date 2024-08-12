"""
Module for managing a singleton instance of SQLAlchemy for database interactions.
"""

from flask_sqlalchemy import SQLAlchemy

# Singleton instance of SQLAlchemy
_DATABASE= None

def get_database():
    """
    Get the singleton instance of SQLAlchemy.

    If the instance does not exist, it is created and initialized.

    Returns:
        SQLAlchemy: The singleton instance of SQLAlchemy.
    """
    global _DATABASE
    if _DATABASE is None:
        _DATABASE = SQLAlchemy()
    return _DATABASE
