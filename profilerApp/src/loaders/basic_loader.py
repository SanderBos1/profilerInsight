
class BasicLoader():
    """
    A Super class that defines the structure of a loader class.

    Attributes:
        - N / A

    """
    
    def __init__(self):
        pass

    def load(self, column):
        """ 
        Load data from a source into a pandas dataframe.

        Returns:
            - A pandas Dataframe containing clean data.    
        """
        raise NotImplementedError("Method not implemented")
    
    def load_examples(self):
        """ 
        Load the first 10 rows of the data into a datframe and converts it to html.

        Returns:
            - A pandas Dataframe containing the first 10 rows of the data.    
        """
        raise NotImplementedError("Method not implemented")
    
    def load_columns(self):
        """ 
        Load the columns of the data into a list
        
        Returns:
            - List: containg the columns that are present in the data.
        """
        raise NotImplementedError("Method not implemented")
