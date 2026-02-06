# Fortune Weather App

A real-time weather application that provides accurate weather forecasts for Nigerian cities and locations worldwide. This app features both frontend and backend components for a complete web application.

## 🌍 Features

- **Real-time Weather Data** - Current weather conditions with temperature, humidity, wind speed, and pressure
- **5-Day Forecast** - Extended weather forecast for planning ahead
- **Multiple Search Methods**:
  - Search by city name
  - Search by coordinates (latitude/longitude)
  - Quick selection of Nigerian cities
- **Detailed Information**:
  - Sunrise/Sunset times
  - Wind speed and direction
  - Cloud coverage
  - Visibility
  - "Feels like" temperature
- **Responsive Design** - Works on desktop, tablet, and mobile devices
- **Protected API Keys** - Backend proxy secures OpenWeatherMap API credentials

## 🛠️ Tech Stack

### Frontend
- HTML5
- CSS3
- Vanilla JavaScript

### Backend
- Python 3.x
- Flask
- Flask-CORS

### APIs
- OpenWeatherMap API

### Hosting
- Frontend: Can be deployed on Netlify, Vercel, or any static host
- Backend: Deployed on Vercel (serverless)

## 📋 Prerequisites

- Python 3.7 or higher
- pip (Python package manager)
- Git

## 🚀 Installation & Setup

### 1. Clone the Repository
```bash
git clone <your-github-repo-url>
cd "Weather App"
```

### 2. Create Virtual Environment
```bash
python -m venv .venv
```

### 3. Activate Virtual Environment

**Windows (PowerShell):**
```powershell
.\.venv\Scripts\Activate.ps1
```

**Windows (Command Prompt):**
```cmd
.venv\Scripts\activate.bat
```

**macOS/Linux:**
```bash
source .venv/bin/activate
```

### 4. Install Dependencies
```bash
pip install -r requirements.txt
```

### 5. Set Up Environment Variables

Create a `.env.local` file in the root directory:
```
OPENWEATHER_API_KEY=your_openweathermap_api_key_here
```

Get your free API key from: https://openweathermap.org/api

## 💻 Running Locally

1. **Activate virtual environment** (if not already activated)
   ```bash
   .\.venv\Scripts\Activate.ps1  # Windows PowerShell
   ```

2. **Start Flask development server**
   ```bash
   flask run
   ```

3. **Open in browser**
   - Go to `http://localhost:5000`
   - You should see the Fortune Weather App homepage

4. **Test the app**
   - Search for a city (e.g., "Lagos")
   - Try different search methods
   - Check the browser console (F12) for any errors

## 📁 Project Structure

```
Weather App/
├── app.py                 # Flask backend application
├── requirements.txt       # Python dependencies
├── vercel.json           # Vercel deployment configuration
├── .env.example          # Example environment variables
├── .env.local            # Local environment variables (not uploaded)
├── .gitignore            # Git ignore rules
├── README.md             # This file
├── templates/
│   └── index.html        # Main HTML file
├── static/
│   ├── style.css         # Styling
│   └── script.js         # Frontend JavaScript
└── .venv/                # Virtual environment (local only)
```

## 🔌 API Endpoints

### Current Weather
```
GET /api/weather/current
```

**Query Parameters:**
- `q` - City name (e.g., `q=Lagos,NG`)
- OR `lat` & `lon` - Latitude and longitude coordinates

**Example:**
```
http://localhost:5000/api/weather/current?q=Lagos,NG
```

### 5-Day Forecast
```
GET /api/weather/forecast
```

**Query Parameters:**
- `q` - City name
- OR `lat` & `lon` - Coordinates

**Example:**
```
http://localhost:5000/api/weather/forecast?q=Lagos,NG
```

## 🌐 Deployment

### Deploy Backend to Vercel

1. **Push code to GitHub**
   ```bash
   git add .
   git commit -m "Initial Flask weather app"
   git push origin main
   ```

2. **Go to Vercel.com**
   - Click "Import Project"
   - Select your GitHub repository
   - Select Python as the framework

3. **Add Environment Variables**
   - In Vercel settings, add:
   - Name: `OPENWEATHER_API_KEY`
   - Value: `your_actual_api_key`

4. **Deploy**
   - Vercel will automatically deploy your Flask backend
   - Get your Vercel URL (e.g., `https://your-project.vercel.app`)

### Update Frontend for Production

Once deployed, update `script.js` to use your Vercel URL:

```javascript
const BACKEND_URL = (window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1')
    ? 'http://localhost:5000' 
    : 'https://your-project.vercel.app';
```

### Deploy Frontend

You can deploy the frontend separately or keep it with the backend:

**Option 1: Same Vercel App (Recommended)**
- Flask serves both frontend and backend
- Single deployment

**Option 2: Separate Netlify/Vercel**
- Deploy frontend to Netlify
- Backend on Vercel
- Update `BACKEND_URL` to point to Vercel

## 🔐 Security Notes

- ✅ API key is protected on backend (not exposed in frontend code)
- ✅ Use environment variables for sensitive data
- ✅ Never commit `.env.local` to GitHub
- ✅ Always use `.env.example` to document required variables
- ✅ CORS is enabled for development but can be restricted in production

## 🐛 Troubleshooting

### ModuleNotFoundError
```bash
pip install -r requirements.txt
```

### "Address already in use" error
- Another Flask instance is running
- Kill the process or use a different port: `flask run --port 5001`

### CORS errors
- Ensure `flask-cors` is installed: `pip install flask-cors`
- Check `BACKEND_URL` in `script.js` matches your Flask server URL

### Weather data not loading
- Check API key is valid in `.env.local`
- Verify API key has OpenWeatherMap API access
- Check browser console for error messages

## 📚 Resources

- [OpenWeatherMap API Docs](https://openweathermap.org/api)
- [Flask Documentation](https://flask.palletsprojects.com/)
- [Vercel Python Deployment](https://vercel.com/docs/runtimes/python)

## 👨‍💼 Author

Fortune Weather App - Created by UGWU JOSHUA CHIMAOBI

## 📄 License

This project is open source and available under the MIT License.

## 🤝 Contributing

Feel free to fork, modify, and submit pull requests for any improvements!

---

**Happy Weather Forecasting! 🌦️**
