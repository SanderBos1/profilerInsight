import numpy as np
import pandas as pd

from src.models import DbConnections, ConnectedTables
from src.database import get_database_connection
from .basic_loader import BasicLoader



class DbLoader(BasicLoader):

    """
    A class that loads data from a database into a pandas DataFrame.

    Attributes:
        - BasicLoader (class): The parent class that defines the structure of a loader class.

    """
    
    def load(self, column, table_id:str) -> pd.DataFrame:
        """
        Load the data from the database into a pandas DataFrame.

        Returns:
            - column_data: A pandas series containing the data of the specified column.
        """
        table_info = ConnectedTables.query.filter_by(table_id=table_id).first()
        table_connection_id = table_info.connection_id
        table_schema = table_info.schemaName
        table_tablename = table_info.tableName
        connection = DbConnections.query.filter_by(connection_id=table_connection_id).first()
        password = connection.password
        connection_dict = connection.to_dict()
        new_db_connection = get_database_connection(connection_dict['db_type'],\
                                                                     connection_dict, password)
        column_data = new_db_connection.get_column_data(table_schema, table_tablename, column)
        column_data = np.array([row[0] for row in column_data])
        column_data = pd.Series(column_data)
        return column_data, table_tablename, table_connection_id
    
    def load_examples(self) -> pd.DataFrame:
        """
        Load the first 10 rows of the database table into a dataframe.

        Returns:
            - df: a DataFrame containing the first 10 rows of the csv file
        """
        return ["test1", "test2", "test3", "test4", "test5", "test6", "test7", "test8", \
                "test9", "test10"]
        
    def load_columns(self, table_id:str) -> list:
        """
        Load the columns of a database  into a list.

        Returns:
            - list: A list containing the column names of the specified table.
        """
        table_info = ConnectedTables.query.filter_by(table_id=table_id).first()
        table_connection_id = table_info.connection_id
        table_tablename = table_info.tableName
        table_schema = table_info.schemaName
        connection = DbConnections.query.filter_by(connection_id=table_connection_id).first()
        password = connection.password
        connection_dict = connection.to_dict()
        new_db_connection = get_database_connection(connection_dict['db_type'], \
                                                                    connection_dict, password)
        answer = new_db_connection.get_table_columns(table_schema, table_tablename)
        return answer
