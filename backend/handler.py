from app import app
from serverless_wsgi import handle_request

def handler(event, context):
    """
    AWS Lambda entry point for Flask app.
    Converts API Gateway HTTP events to WSGI requests using serverless-wsgi.
    """
    return handle_request(app, event, context)
