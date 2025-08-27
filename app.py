"""
AI Interview Prepper - Modern Flask Application
Entry point using application factory pattern
"""
import os
from app import create_app
from app.core.config import config

# Get configuration from environment
config_name = os.environ.get('FLASK_CONFIG', 'development')
app = create_app(config[config_name])

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)