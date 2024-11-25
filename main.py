import os
from flask import Flask, render_template, redirect, request, session
import random
import string

app = Flask(__name__)

# Use environment variable for secret key, or fallback to a default value if not set
app.secret_key = os.environ.get('SECRET_KEY', 'your_default_secret_key')

# Determine whether to run in debug mode based on the environment
app.config['DEBUG'] = os.environ.get('FLASK_DEBUG', 'False') == 'True'

def generate_password(length=12):
    """Generates a random password with letters, digits, and punctuation"""
    chars = string.ascii_letters + string.digits + string.punctuation
    password = ''.join(random.choice(chars) for _ in range(length))
    return password

@app.route("/", methods=["GET", "POST"])
def index():
    # Retrieve the password from the session if available
    password = session.get('password', None)
    
    if request.method == "POST":
        # Get password length from the form, defaulting to 12 if not provided
        length = int(request.form.get('length', 12))
        
        # Generate a new password based on the chosen length
        password = generate_password(length)
        
        # Store the generated password in the session
        session['password'] = password

        return render_template("index.html", password=password)
    
    return render_template("index.html", password=password)

if __name__ == "__main__":
    app.run(debug=app.config['DEBUG'])  # Runs with debug based on the environment setting
