"""
Module for registering custom error handlers for the Flask application.
"""

from flask import jsonify

def register_error_handlers(app):
    """
    Register custom error handlers for the Flask application.

    This function sets up error handling for specific HTTP status codes,
    allowing the application to return a JSON response with a custom message.

    Args:
        app (Flask): The Flask application instance to register error handlers with.

    Returns:
        None
    """
    @app.errorhandler(404)
    def not_found():
        """
        Handle 404 Not Found errors.

        Returns:
            Response: A JSON response with a message indicating that the endpoint was not found,
                      and an HTTP status code of 404.
        """
        return jsonify({'message': 'Endpoint not found'}), 404
