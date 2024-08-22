import logging

from flask import Blueprint, jsonify, request
from sqlalchemy.exc import OperationalError, IntegrityError
from marshmallow import ValidationError

from src.models import QualityRules, ConnectedTables
from src.config import SingletonDB
from src.data_quality import QualityRuleFactory
from src.data_quality.data_quality_calculator import calculate_data_quality
from src.schemas.quality_rule_schema import QualityRuleSchema

DB = SingletonDB.get_instance()


data_quality_bp = Blueprint(
    "data_quality_bp",
    __name__,
)


@data_quality_bp.route("/api/get_quality_rules", methods=["get"])
def get_quality_rules():
    """
    Get all quality rules.

    This function retrieves all quality rules from the database.

    Returns:
        Response: A JSON response containing all quality rules.
    """
    data_quality_calculator = QualityRuleFactory()
    existing_rules = data_quality_calculator.get_existing_rules()
    return jsonify({"Answer":existing_rules})
    

@data_quality_bp.route("/api/get_quality_rules/<table_id>", methods=["get"])
def get_quality_rules_table(table_id):
    """
    Get the quality rules for a specific table.

    This function retrieves the quality rules for a specific table from the database.

    Args:
        table_id (int): The unique identifier of the table.

    Returns:
        Response: A JSON response containing the quality rules for the table.
    """
    try:
        querry = DB.session.query(QualityRules).filter_by(table_id=table_id) \
            .group_by(QualityRules.rule_id, QualityRules.column_name)
        quality_rules = querry.all()
        quality_rules_list = [rule.to_dict() for rule in quality_rules]
        return jsonify({"Answer": quality_rules_list})
    except OperationalError as e:
        logging.error(f"Error retrieving quality rules: {e}")
        return jsonify({"Error": "Error retrieving quality rules"}), 500
    
@data_quality_bp.route("/api/add_rule", methods=["POST"])
def add_quality_rule():
    """
    Add a quality rule for a specific table.

    This function adds a quality rule for a specific table to the database.

    Args:
        table_id (int): The unique identifier of the table.

    Returns:
        Response: A JSON response indicating success or failure.
    """
    try:
        connection_schema = QualityRuleSchema()
        data = connection_schema.load(request.get_json())
    except ValidationError as e:
        logging.error('Validation Error: %s', e)
        return jsonify({"Error": "Incorrect Data"}), 400
    try:
        table_id = data["table_id"]
        rule_name = data["rule_name"]
        column_name = data["column_name"]
        threshold = data["threshold"]
        if "extra_info" in data:
            extra_info = data["extra_info"]
        else:
            extra_info = ""
        connection_id = DB.session.query(ConnectedTables).filter_by(table_id=table_id).first().connection_id
        quality_rule = QualityRules(
            table_id=table_id,
            connection_id=connection_id,
            quality_rule=rule_name,
            column_name=column_name,
            threshold=threshold,
            extra_info = extra_info
        )
        DB.session.add(quality_rule)
        DB.session.commit()
        return jsonify({"Message": "Quality rule added successfully"})
    except OperationalError as e:
        logging.error(f"Error adding quality rule: {e}")
        return jsonify({"Error": "Error adding quality rule"}), 500

@data_quality_bp.route("/api/delete_rule/<rule_id>", methods=["DELETE"])
def delete_quality_rule(rule_id):
    """
    Delete a quality rule for a specific table.

    This function deletes a quality rule for a specific table from the database.

    Args:
        table_id (int): The unique identifier of the table.

    Returns:
        Response: A JSON response indicating success or failure.
    """

    try:
        rule = QualityRules.query.filter_by(rule_id=rule_id).first()
        if rule is None:
            return jsonify({'Error': 'Rule not found'}), 404
        DB.session.delete(rule)
        DB.session.commit()
        return jsonify({'Message':"Quality rule deleted successfully"}), 200
    except IntegrityError as e:
        DB.session.rollback()
        logging.error('Integrity error: %s', e)
        return jsonify({"Error": "Rule not found"}), 403
    except OperationalError as e:
        logging.error('Database error occurred: %s', e)
        return jsonify({"Error": "Database operation failed"}), 500


@data_quality_bp.route("/api/calculate_quality/<table_id>", methods=["GET"])
def calculate_quality(table_id):
    """
    Calculate the quality of a table.

    This function calculates the quality of a table based on the quality rules
    defined for the table.

    Returns:
        Response: A JSON response containing the quality of the table.
    """
    try:
        calculate_data_quality(table_id)
        return jsonify({"Message": "quality calculated successfully"})
    except OperationalError as e:
        logging.error(f"Error calculating quality: {e}")
        return jsonify({"Error": "Error calculating quality"}), 500
