"""Rendering contact page."""
from flask import render_template

from app import app
from config import user_loggined


@app.route('/contact', methods=['GET', 'POST'])
def contact():
    """Rendering contact page."""
    return render_template('contact.html', loggined=user_loggined())

