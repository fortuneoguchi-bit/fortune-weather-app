from flask import Flask, jsonify, request, render_template
from flask_cors import CORS
import requests
import os

app = Flask(__name__, 
            template_folder='templates',
            static_folder='static',
            static_url_path='/static')
CORS(app)

# API key should be in environment variable (not exposed in code)
API_KEY = os.environ.get('OPENWEATHER_API_KEY', '49914b80874f44e48ec15a7026a654a4')
BASE_URL = 'https://api.openweathermap.org/data/2.5'

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/api/weather/current', methods=['GET'])
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
