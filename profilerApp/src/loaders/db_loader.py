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
    def  get_connection_info(self, table_id:str) -> dict:
        """
        Get the connection information for a table.

        Args:
            - table_id (str): The ID of the table.

        Returns:
            - connection_dict (dict): A dictionary containing the connection information.
        """
        table_info = ConnectedTables.query.filter_by(table_id=table_id).first()
        table_info = table_info.to_dict()
        table_connection_id = table_info['connection_id']
        connection = DbConnections.query.filter_by(connection_id=table_connection_id).first()
        password = connection.password
        connection_dict = connection.to_dict()
        return connection_dict, table_info, password
    
    def load(self, column, table_id:str) -> pd.DataFrame:
        """
        Load the data from the database into a pandas DataFrame.

        Returns:
            - column_data: A pandas series containing the data of the specified column.
        """
        connection_dict, table_info, password = self.get_connection_info(table_id)
        new_db_connection = get_database_connection(connection_dict['db_type'],\
                                                                     connection_dict, password)
        column_data = new_db_connection.get_column_data(table_info['schema_name'], table_info['table_name'], column)
        column_data = np.array([row[0] for row in column_data])
        column_data = pd.Series(column_data)
        return column_data, table_info['table_name'], table_info['connection_id']
    
    def load_examples(self, table_id:str) -> pd.DataFrame:
        """
        Load the first 10 rows of the database table into a dataframe.

        Returns:
            - df: a DataFrame containing the first 10 rows of the csv file
        """
        connection_dict, table_info, password = self.get_connection_info(table_id)

        new_db_connection = get_database_connection(connection_dict['db_type'],\
                                                                     connection_dict, password)
        preview = new_db_connection.get_preview_data(table_info['schema_name'], table_info['table_name'])      
        columns = new_db_connection.get_table_columns(table_info['schema_name'], table_info['table_name'])      
        df = pd.DataFrame(preview, columns=columns)
        preview = df.to_html(index=False, classes=["table table-bordered", \
                                                                   "table-striped", "table-hover"])
        return preview
        
    def load_columns(self, table_id:str) -> list:
        """
        Load the columns of a database  into a list.

        Returns:
            - list: A list containing the column names of the specified table.
        """
        connection_dict, table_info, password = self.get_connection_info(table_id)

        new_db_connection = get_database_connection(connection_dict['db_type'], \
                                                                    connection_dict, password)
        answer = new_db_connection.get_table_columns(table_info['schema_name'], table_info['table_name'])
        return answer
