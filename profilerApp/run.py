from src import create_app
import os 
from gevent import pywsgi

app = create_app("development")
# app = create_app("test")
# app = create_app()

if __name__ == '__main__':
    host = os.getenv('FLASK_HOST', '127.0.0.1')
    port = int(os.getenv('FLASK_PORT', 5000))
    
    http_server = pywsgi.WSGIServer(
        (host, port),
        app,
    )
    http_server.serve_forever()


