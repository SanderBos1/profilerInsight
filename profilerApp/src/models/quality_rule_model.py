from src.config import SingletonDB

DB = SingletonDB.get_instance()

class QualityRules(DB.Model):
    """
    Represent a table that is connected to a specific database connection.

    This class is an SQLAlchemy model that defines the schema for storing information about tables
    associated with particular database connections.

    Attributes:
        table_id (int): Unique identifier for the table entry.
        connection_id (str): Identifier of the associated database connection.
        rule_name (str): Name of the rule.
        column_name (str): Name of the column.
        extra_info (str): Additional information about the rule.

    Methods:
        to_dict: Converts the model instance to a dictionary.
    """
    rule_id = DB.Column(DB.Integer, primary_key=True)
    table_id = DB.Column(DB.Integer, nullable=False)
    connection_id = DB.Column(DB.String(80), nullable=False)
    quality_rule = DB.Column(DB.String(80), nullable=False)
    column_name = DB.Column(DB.String(80), nullable=False)
    threshold = DB.Column(DB.Float, nullable=False)
    extra_info = DB.Column(DB.String(80), nullable=True)
    calculated_threshold = DB.Column(DB.Float, nullable=True)
    succeded = DB.Column(DB.Boolean, nullable=False, default=False)

    def to_dict(self):
        """
        Convert the ConnectedTables instance to a dictionary representation.

        The dictionary includes all attributes of the instance.

        Returns:
            dict: A dictionary representation of the ConnectedTables instance.
        """
        quality_rules_dict = {
            "rule_id": self.rule_id,
            "table_id": self.table_id,
            "connection_id": self.connection_id,
            "quality_rule": self.quality_rule,
            "column_name": self.column_name,
            "threshold": self.threshold,
            "extra_info": self.extra_info,
            "calculated_threshold": self.calculated_threshold,
            "succeded": self.succeded   
        }
        return quality_rules_dict