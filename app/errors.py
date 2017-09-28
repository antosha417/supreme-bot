"""Rendering error page."""
from flask import render_template

from app import app


@app.errorhandler(500)
def internal_error(error):
    """Handel internal_error."""
    print error
    return render_template('error.html'), 500


@app.errorhandler(404)
def not_found(error):
    """Handel not_found error."""
    print error
    return render_template('error.html'), 404

