# Vercel Entry Point
from dotenv import load_dotenv
from app import app
import os

load_dotenv()

if __name__ == "__main__":
    env = os.getenv('FLASK_ENV')
    if env == 'development':
        app.run(debug=True)
    else:
        app.run()