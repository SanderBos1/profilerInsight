"""
Module for registering custom error handlers for the Flask application.
"""

from flask import Blueprint, jsonify

errors_bp = Blueprint(
    "errors_bp",
    __name__
)


@errors_bp.app_errorhandler(404)
def handle_404(e):
    """
    Handle 404 Not Found errors.

    Returns:
        Response: A JSON response with a message indicating that the endpoint was not found,
        and an HTTP status code of 404.

    """
    return jsonify({'Message': 'Endpoint not found'}), 404
