"""
The flask application package.
"""

from flask import Flask
app = Flask(__name__)

import FlaskWebsite.views
# import FlaskWebsite.data.twitter
