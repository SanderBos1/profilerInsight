class Database:
    def __init__(self, connection_details):
        self.connection_details = connection_details

    def connect(self):
        raise NotImplementedError("This method should be overridden by subclasses")

    def execute_query(self, query:str):
        raise NotImplementedError("This method should be overridden by subclasses")
    
    def get_all_tables(self):
        raise NotImplementedError("This method should be overridden by subclasses")
    
    
