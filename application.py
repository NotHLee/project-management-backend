"""
application.py contains the app variable to be shared across all routes.
"""
from flask import Flask

# Application to be shared across all routes
app = Flask(__name__)