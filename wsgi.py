"""
This is the file which is provided to FLASK_APP env variable
"""
import os
from application import create_app

app = create_app(os.getenv("FLASK_ENV") or "test")
