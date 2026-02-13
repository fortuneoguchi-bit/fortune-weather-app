from flask import Flask, jsonify, request, render_template, redirect, url_for, session, flash
from flask_cors import CORS
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps
import requests
import sqlite3
import os

app = Flask(__name__, 
            template_folder='templates',
            static_folder='static',
            static_url_path='/static')
app.secret_key = os.environ.get('SECRET_KEY', 'fortune-weather-app-secret-key-2025')
CORS(app)

# API key should be in environment variable (not exposed in code)
API_KEY = os.environ.get('OPENWEATHER_API_KEY', '49914b80874f44e48ec15a7026a654a4')
BASE_URL = 'https://api.openweathermap.org/data/2.5'

# Database path
DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'weather_users.db')

# ─── Database Helpers ────────────────────────────────────────────────

def get_db():
    """Get a database connection."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    """Create users table if it doesn't exist."""
    conn = get_db()
    conn.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()

# Initialize the database on startup
init_db()

# ─── Auth Decorator ──────────────────────────────────────────────────

def login_required(f):
    """Decorator to protect routes that require authentication."""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            # For API routes, return 401 JSON
            if request.path.startswith('/api/'):
                return jsonify({'error': 'Authentication required'}), 401
            # For page routes, redirect to auth
            return redirect(url_for('auth_page'))
        return f(*args, **kwargs)
    return decorated_function

# ─── Auth Routes ─────────────────────────────────────────────────────

@app.route('/auth')
def auth_page():
    """Render the sign-in / sign-up page."""
    if 'user_id' in session:
        return redirect(url_for('home'))
    return render_template('auth.html')

@app.route('/auth/signup', methods=['POST'])
def signup():
    """Register a new user."""
    name = request.form.get('name', '').strip()
    email = request.form.get('email', '').strip().lower()
    password = request.form.get('password', '')

    # Validation
    if not name or not email or not password:
        flash('All fields are required.', 'error')
        return redirect(url_for('auth_page') + '?tab=signup')

    if len(password) < 6:
        flash('Password must be at least 6 characters.', 'error')
        return redirect(url_for('auth_page') + '?tab=signup')

    try:
        conn = get_db()
        # Check if email already exists
        existing = conn.execute('SELECT id FROM users WHERE email = ?', (email,)).fetchone()
        if existing:
            conn.close()
            flash('An account with this email already exists.', 'error')
            return redirect(url_for('auth_page') + '?tab=signup')

        # Create user
        hashed_password = generate_password_hash(password)
        cursor = conn.execute(
            'INSERT INTO users (name, email, password) VALUES (?, ?, ?)',
            (name, email, hashed_password)
        )
        conn.commit()
        user_id = cursor.lastrowid
        conn.close()

        # Auto-login after signup
        session['user_id'] = user_id
        session['user_name'] = name
        session['user_email'] = email
        flash(f'Welcome, {name}! Account created successfully.', 'success')
        return redirect(url_for('home'))

    except Exception as e:
        flash('An error occurred. Please try again.', 'error')
        return redirect(url_for('auth_page') + '?tab=signup')

@app.route('/auth/signin', methods=['POST'])
def signin():
    """Authenticate an existing user."""
    email = request.form.get('email', '').strip().lower()
    password = request.form.get('password', '')

    if not email or not password:
        flash('Please enter both email and password.', 'error')
        return redirect(url_for('auth_page'))

    try:
        conn = get_db()
        user = conn.execute('SELECT * FROM users WHERE email = ?', (email,)).fetchone()
        conn.close()

        if not user or not check_password_hash(user['password'], password):
            flash('Invalid email or password.', 'error')
            return redirect(url_for('auth_page'))

        # Set session
        session['user_id'] = user['id']
        session['user_name'] = user['name']
        session['user_email'] = user['email']
        flash(f'Welcome back, {user["name"]}!', 'success')
        return redirect(url_for('home'))

    except Exception as e:
        flash('An error occurred. Please try again.', 'error')
        return redirect(url_for('auth_page'))

@app.route('/auth/logout')
def logout():
    """Log out the current user."""
    session.clear()
    flash('You have been logged out.', 'info')
    return redirect(url_for('auth_page'))

# ─── Weather Routes (Protected) ─────────────────────────────────────

@app.route('/')
@login_required
def home():
    return render_template('index.html', user_name=session.get('user_name', 'User'))

@app.route('/api/weather/current', methods=['GET'])
@login_required
def get_current_weather():
    """
    Get current weather data
    Query params: q (city), lat (latitude), lon (longitude)
    """
    try:
        # Get query parameters
        city = request.args.get('q')
        lat = request.args.get('lat')
        lon = request.args.get('lon')
        
        if not city and not (lat and lon):
            return jsonify({'error': 'Please provide city name or coordinates'}), 400
        
        # Build query
        if city:
            query = f"q={city}"
        else:
            query = f"lat={lat}&lon={lon}"
        
        # Call OpenWeatherMap API
        url = f"{BASE_URL}/weather?{query}&appid={API_KEY}&units=metric"
        response = requests.get(url, timeout=10)
        
        if response.status_code != 200:
            return jsonify({'error': 'City not found or invalid coordinates'}), response.status_code
        
        return jsonify(response.json())
    
    except requests.exceptions.RequestException as e:
        return jsonify({'error': str(e)}), 500
    except Exception as e:
        return jsonify({'error': 'An error occurred'}), 500

@app.route('/api/weather/forecast', methods=['GET'])
@login_required
def get_forecast():
    """
    Get 5-day forecast data
    Query params: q (city), lat (latitude), lon (longitude)
    """
    try:
        # Get query parameters
        city = request.args.get('q')
        lat = request.args.get('lat')
        lon = request.args.get('lon')
        
        if not city and not (lat and lon):
            return jsonify({'error': 'Please provide city name or coordinates'}), 400
        
        # Build query
        if city:
            query = f"q={city}"
        else:
            query = f"lat={lat}&lon={lon}"
        
        # Call OpenWeatherMap API
        url = f"{BASE_URL}/forecast?{query}&appid={API_KEY}&units=metric"
        response = requests.get(url, timeout=10)
        
        if response.status_code != 200:
            return jsonify({'error': 'Unable to fetch forecast data'}), response.status_code
        
        return jsonify(response.json())
    
    except requests.exceptions.RequestException as e:
        return jsonify({'error': str(e)}), 500
    except Exception as e:
        return jsonify({'error': 'An error occurred'}), 500

if __name__ == '__main__':
    app.run(debug=True)
