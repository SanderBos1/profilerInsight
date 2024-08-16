"""
Main entry point for the Flask application using Gevent's WSGI server.

"""
import os
from gevent import pywsgi
from src import create_app

def main():
    """
    Create and run the Flask application using Gevent's WSGI server.

    The application is created based on the environment configuration:
    - 'development'
    - 'test' (commented out)
    - 'production' (commented out)

    Environment variables:
    - FLASK_HOST: The host address to bind the server to (default is '127.0.0.1').
    - FLASK_PORT: The port number to bind the server to (default is '5000').
    """
    # app = create_app("development")
    # app = create_app("test")
    app = create_app("production")

    host = os.getenv('FLASK_HOST', '127.0.0.1')
    port = int(os.getenv('FLASK_PORT', '5000'))

    http_server = pywsgi.WSGIServer(
        (host, port),
        app,
    )

    print(f"Starting server on {host}:{port}")
    http_server.serve_forever()

if __name__ == '__main__':
    main()
