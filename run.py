"""
run.py, the main driver function for the backend, starts the flask server with all routes connected.
"""
from application import app
from flask_cors import CORS
from controllers import *
from policies import *

CORS(app, origin='*')

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5000)