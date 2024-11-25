import os
from flask import Flask, render_template, redirect, request, session
import random
import string

app = Flask(__name__)

# Use environment variable for secret key, or fallback to a default value if not set
app.secret_key = os.environ.get('SECRET_KEY', 'your_default_secret_key')

# Determine whether to run in debug mode based on the environment
app.config['DEBUG'] = os.environ.get('FLASK_DEBUG', 'False') == 'True'

shortened_urls = {}

def generate_short_url(length=6):
    chars = string.ascii_letters + string.digits
    short_url = ''.join(random.choice(chars) for _ in range(length))
    return short_url

@app.route("/", methods=["GET", "POST"])
def index():
    # Retrieve the short_url from the session if available
    short_url = session.get('short_url', None)
    
    if request.method == "POST":
        long_url = request.form['long_url']
        short_url = generate_short_url()
        while short_url in shortened_urls:
            short_url = generate_short_url()

        shortened_urls[short_url] = long_url

        # Store the generated short_url in the session for this user
        session['short_url'] = f"{request.url_root}{short_url}"

        return render_template("index.html", short_url=session['short_url'])
    
    return render_template("index.html", short_url=short_url)

@app.route("/<short_url>")
def redirect_url(short_url):
    long_url = shortened_urls.get(short_url)
    if long_url:
        return redirect(long_url)
    else:
        return "URL not found", 404

if __name__ == "__main__":
    app.run(debug=app.config['DEBUG'])  # Runs with debug based on the environment setting
