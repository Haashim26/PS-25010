import streamlit as st
import numpy as np
from PIL import Image
import json
import requests
from datetime import datetime, timedelta
import pandas as pd
import matplotlib.pyplot as plt
import pyttsx3
from googletrans import Translator
import os
import time

# Set page configuration
st.set_page_config(
    page_title="AgriSathi - Smart Crop Advisory",
    page_icon="🌱",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        color: #2e7d32;
        text-align: center;
        margin-bottom: 2rem;
    }
    .sub-header {
        font-size: 1.8rem;
        color: #388e3c;
        border-bottom: 2px solid #c8e6c9;
        padding-bottom: 0.5rem;
        margin-top: 1.5rem;
    }
    .card {
        background-color: #f1f8e9;
        border-radius: 10px;
        padding: 1.5rem;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        margin-bottom: 1.5rem;
    }
    .urgent-alert {
        background-color: #ffebee;
        border-left: 5px solid #f44336;
        padding: 1rem;
        border-radius: 5px;
        margin-bottom: 1rem;
    }
    .weather-alert {
        background-color: #fff3e0;
        border-left: 5px solid #ff9800;
        padding: 1rem;
        border-radius: 5px;
        margin-bottom: 1rem;
    }
    .big-button {
        display: block;
        width: 100%;
        padding: 1rem;
        background-color: #4caf50;
        color: white;
        border: none;
        border-radius: 5px;
        font-size: 1.2rem;
        margin: 0.5rem 0;
        cursor: pointer;
        text-align: center;
    }
    .big-button:hover {
        background-color: #388e3c;
    }
    .crop-card {
        background: linear-gradient(to bottom right, #e8f5e9, #c8e6c9);
        border-radius: 10px;
        padding: 1rem;
        margin: 0.5rem 0;
    }
    .market-up {
        color: #4caf50;
    }
    .market-down {
        color: #f44336;
    }
    .market-same {
        color: #ff9800;
    }
    @media (max-width: 768px) {
        .main-header {
            font-size: 2rem;
        }
    }
</style>
""", unsafe_allow_html=True)

# UI Translation
ui_text = {
    "en": {
        "title": "AgriSathi - Smart Crop Advisory",
        "welcome": "Welcome to your digital farming assistant",
        "disease_detection": "Disease Detection",
        "crop_advisory": "Crop Advisory",
        "market_prices": "Market Prices",
        "weather_info": "Weather Info",
        "soil_health": "Soil Health",
        "select_city": "Select your district/city",
        "select_language": "Select Language",
        "select_crop": "Select your crop",
        "take_picture": "Take Picture of Plant",
        "upload_image": "Or upload image",
        "analyze": "Analyze Plant Health",
        "prediction_result": "Detection Result",
        "advice": "Recommended Action",
        "prevention": "Prevention Tips",
        "weather_forecast": "Weather Forecast",
        "soil_tips": "Soil Health Tips",
        "market_trends": "Price Trends",
        "submit_feedback": "Submit Feedback",
        "feedback_placeholder": "Share your experience or suggestions...",
        "voice_output": "Listen to Advice",
        "soil_type": "Soil Type",
        "best_season": "Best Season",
        "water_needs": "Water Needs",
        "ph_level": "Optimal pH Level",
        "common_pests": "Common Pests",
        "expert_help": "Connect with Expert",
        "alert": "Important Alert",
        "rain_alert": "Heavy rain expected in next 3 days. Harvest mature crops immediately.",
        "temp_alert": "High temperature warning. Water plants in early morning or late evening.",
        "wind_alert": "Strong winds expected. Secure loose structures and protect young plants.",
        "phone_label": "Phone Number",
        "question_label": "Your Question",
        "submit_question": "Submit Question",
        "thank_you": "Thank you! An expert will contact you within 24 hours.",
        "real_time_data": "Real-time Data",
        "last_updated": "Last updated",
        "refresh_data": "Refresh Data",
        "expert_advice": "Expert Advice",
        "community_forum": "Community Forum",
        "gov_schemes": "Government Schemes",
        "weather_warnings": "Weather Warnings",
        "market_analysis": "Market Analysis",
        "crop_calendar": "Crop Calendar"
    },
    "hi": {
        "title": "AgriSathi - स्मार्ट फसल सलाह",
        "welcome": "आपके डिजिटल फार्मिंग सहायक में आपका स्वागत है",
        "disease_detection": "रोग पहचान",
        "crop_advisory": "फसल सलाह",
        "market_prices": "बाजार मूल्य",
        "weather_info": "मौसम जानकारी",
        "soil_health": "मृदा स्वास्थ्य",
        "select_city": "अपना जिला/शहर चुनें",
        "select_language": "भाषा चुनें",
        "select_crop": "अपनी फसल चुनें",
        "take_picture": "पौधे की तस्वीर लें",
        "upload_image": "या छवि अपलोड करें",
        "analyze": "पौधे का स्वास्थ्य जांचें",
        "prediction_result": "परिणाम",
        "advice": "सुझाव",
        "prevention": "रोकथाम के उपाय",
        "weather_forecast": "मौसम पूर्वानुमान",
        "soil_tips": "मृदा स्वास्थ्य सुझाव",
        "market_trends": "मूल्य रुझान",
        "submit_feedback": "प्रतिक्रिया भेजें",
        "feedback_placeholder": "अपना अनुभव या सुझाव साझा करें...",
        "voice_output": "सलाह सुनें",
        "soil_type": "मिट्टी का प्रकार",
        "best_season": "उपयुक्त मौसम",
        "water_needs": "पानी की आवश्यकता",
        "ph_level": "उपयुक्त pH स्तर",
        "common_pests": "सामान्य कीट",
        "expert_help": "विशेषज्ञ से संपर्क करें",
        "alert": "महत्वपूर्ण चेतावनी",
        "rain_alert": "अगले 3 दिनों में भारी बारिश की संभावना। पके हुए फसलों की तुरंत कटाई करें।",
        "temp_alert": "उच्च तापमान चेतावनी। पौधों को सुबह जल्दी या शाम को पानी दें।",
        "wind_alert": "तेज हवाओं की संभावना। ढीली संरचनाओं को सुरक्षित करें और युवा पौधों की रक्षा करें।",
        "phone_label": "फोन नंबर",
        "question_label": "आपका प्रश्न",
        "submit_question": "प्रश्न भेजें",
        "thank_you": "धन्यवाद! एक विशेषज्ञ 24 घंटे के भीतर आपसे संपर्क करेगा।",
        "real_time_data": "रीयल-टाइम डेटा",
        "last_updated": "अंतिम अपडेट",
        "refresh_data": "डेटा रिफ्रेश करें",
        "expert_advice": "विशेषज्ञ सलाह",
        "community_forum": "कम्युनिटी फोरम",
        "gov_schemes": "सरकारी योजनाएं",
        "weather_warnings": "मौसम चेतावनी",
        "market_analysis": "बाजार विश्लेषण",
        "crop_calendar": "फसल कैलेंडर"
    },
    "pa": {
        "title": "AgriSathi - ਸਮਾਰਟ ਫਸਲ ਸਲਾਹ",
        "welcome": "ਤੁਹਾਡੇ ਡਿਜੀਟਲ ਖੇਤੀ ਸहਾਇਕ ਵਿੱਚ ਸਵਾਗਤ ਹੈ",
        "disease_detection": "ਰੋਗ ਪਛਾਣ",
        "crop_advisory": "ਫਸਲ ਸलਾਹ",
        "market_prices": "ਬਾਜ਼ਾਰ ਮੁੱਲ",
        "weather_info": "ਮੌਸਮ ਜਾਣਕਾਰੀ",
        "soil_health": "ਮਿੱਟੀ ਦਾ ਸਿਹਤ",
        "select_city": "ਆਪਣਾ ਜ਼ਿਲ੍ਹਾ/ਸ਼ਹਿਰ ਚੁਣੋ",
        "select_language": "ਭਾਸ਼ਾ ਚੁਣੋ",
        "select_crop": "ਆਪਣੀ ਫਸल ਚੁਣੋ",
        "take_picture": "ਪੌਦੇ ਦੀ ਤਸਵੀਰ ਲਓ",
        "upload_image": "ਜਾਂ ਚਿੱਤਰ ਅੱਪਲੋਡ ਕਰੋ",
        "analyze": "ਪੌਦੇ ਦੀ ਸਿਹਤ ਦੀ ਜਾਂਚ ਕਰੋ",
        "prediction_result": "ਨਤੀਜਾ",
        "advice": "ਸਿਫਾਰਸ਼",
        "prevention": "ਰੋਕਥਾਮ ਦੇ ਉਪਾਅ",
        "weather_forecast": "ਮੌਸਮ ਦਾ ਪੂਰਵਾਨੁਮਾਨ",
        "soil_tips": "ਮਿੱਟੀ ਦੀ ਸਿਹਤ ਲਈ ਸਲਾਹ",
        "market_trends": "ਕੀਮਤ ਰੁਝਾਨ",
        "submit_feedback": "ਪ੍ਰਤਿਕਿਰਿਆ ਦਿਓ",
        "feedback_placeholder": "ਆਪਣਾ ਤਜਰਬਾ ਜਾਂ ਸੁਝਾਅ ਸਾਂਝਾ ਕਰੋ...",
        "voice_output": "ਸलਾਹ ਸੁਣੋ",
        "soil_type": "ਮਿੱਟੀ ਦੀ ਕਿਸਮ",
        "best_season": "ਵਧੀਆ ਮੌਸਮ",
        "water_needs": "ਪਾਣੀ ਦੀ ਲੋੜ",
        "ph_level": "ਵਧੀਆ pH ਪੱਧਰ",
        "common_pests": "ਆਮ ਕੀੜੇ",
        "expert_help": "ਮਾਹਿਰ ਨਾਲ ਜੁੜੋ",
        "alert": "ਮਹੱਤਵਪੂਰਨ ਚੇਤਾਵਨੀ",
        "rain_alert": "ਅਗਲੇ 3 ਦਿਨਾਂ ਵਿੱਚ ਭਾਰੀ ਬਾਰਸ਼ ਦੀ ਸੰਭਾਵਨਾ। ਪੱਕੇ ਹੋਏ ਫਸਲਾਂ ਦੀ ਤੁਰੰਤ ਕਟਾਈ ਕਰੋ।",
        "temp_alert": "ਉੱਚ ਤਾਪਮਾਨ ਚੇਤਾਵਨੀ। ਪੌਦਿਆਂ ਨੂੰ ਸਵੇਰੇ ਜਲਦੀ ਜਾਂ ਸ਼ਾਮ ਨੂੰ ਪਾਣੀ ਦਿਓ।",
        "wind_alert": "ਤੇਜ਼ ਹਵਾਵਾਂ ਦੀ ਉਮੀਦ ਹੈ। ਢਿੱਲੀਆਂ structureਾਂ ਨੂੰ ਸੁਰੱਖਿਅਤ ਕਰੋ ਅਤੇ ਨੌਜਵਾਨ ਪੌਦਿਆਂ ਦੀ ਰੱਖਿਆ ਕਰੋ।",
        "phone_label": "ਫੋਨ ਨੰਬਰ",
        "question_label": "ਤੁਹਾਡਾ ਸਵਾਲ",
        "submit_question": "ਸਵਾਲ ਦਾਖਲ ਕਰੋ",
        "thank_you": "ਧੰਨਵਾਦ! ਇੱਕ ਮਾਹਿਰ 24 ਘੰਟੇ ਦੇ ਅੰਦਰ ਤੁਹਾਡੇ ਨਾਲ ਸੰਪਰਕ ਕਰੇਗਾ।",
        "real_time_data": "ਰੀਅਲ-ਟਾਈਮ ਡੇਟਾ",
        "last_updated": "ਆਖਰੀ ਅੱਪਡੇਟ",
        "refresh_data": "ਡੇਟਾ ਤਾਜ਼ਾ ਕਰੋ",
        "expert_advice": "ਮਾਹਿਰ ਸਲਾਹ",
        "community_forum": "ਕਮਿਊਨਿਟੀ ਫੋਰਮ",
        "gov_schemes": "ਸਰਕਾਰੀ ਸਕੀਮਾਂ",
        "weather_warnings": "ਮੌਸਮ ਚੇਤਾਵਨੀ",
        "market_analysis": "ਮਾਰਕੀਟ ਵਿਸ਼ਲੇਸ਼ਣ",
        "crop_calendar": "ਫਸਲ ਕੈਲੰਡਰ"
    }
}

# Initialize translator
translator = Translator()

# Initialize text-to-speech engine
try:
    tts_engine = pyttsx3.init()
    tts_available = True
except:
    tts_available = False

# Function to translate text
def translate_text(text, dest_lang):
    try:
        if dest_lang == "en":
            return text
        translated = translator.translate(text, dest=dest_lang)
        return translated.text
    except:
        return text

# Function to speak text
def speak_text(text, lang):
    if not tts_available:
        return
        
    try:
        # Set voice properties based on language
        if lang == "hi":
            # Try to set Hindi voice if available
            voices = tts_engine.getProperty('voices')
            for voice in voices:
                if "hindi" in voice.name.lower() or "india" in voice.name.lower():
                    tts_engine.setProperty('voice', voice.id)
                    break
        elif lang == "pa":
            # Try to set Punjabi voice if available
            voices = tts_engine.getProperty('voices')
            for voice in voices:
                if "punjabi" in voice.name.lower() or "india" in voice.name.lower():
                    tts_engine.setProperty('voice', voice.id)
                    break
        
        tts_engine.say(text)
        tts_engine.runAndWait()
    except Exception as e:
        st.sidebar.warning("Voice output not available")

# Weather API Integration
def get_weather_data(city_name):
    """
    Fetch weather data from OpenWeatherMap API
    Note: You need to sign up for a free API key at https://openweathermap.org/
    """
    # Replace with your actual API key
    API_KEY = "YOUR_OPENWEATHERMAP_API_KEY"
    
    if API_KEY == "YOUR_OPENWEATHERMAP_API_KEY":
        # Return mock data if no API key is provided
        return get_mock_weather_data(city_name)
    
    try:
        # First, get the coordinates for the city
        geo_url = f"http://api.openweathermap.org/geo/1.0/direct?q={city_name},IN&limit=1&appid={API_KEY}"
        geo_response = requests.get(geo_url).json()
        
        if not geo_response:
            return get_mock_weather_data(city_name)
            
        lat = geo_response[0]['lat']
        lon = geo_response[0]['lon']
        
        # Then, get the weather data
        weather_url = f"https://api.openweathermap.org/data/2.5/forecast?lat={lat}&lon={lon}&appid={API_KEY}&units=metric"
        weather_response = requests.get(weather_url).json()
        
        if 'list' not in weather_response:
            return get_mock_weather_data(city_name)
            
        # Process the weather data
        current_weather = weather_response['list'][0]
        forecast_data = []
        
        # Get one forecast per day for the next 5 days
        for i in range(0, min(40, len(weather_response['list'])), 8):
            forecast = weather_response['list'][i]
            forecast_data.append({
                'day': datetime.fromtimestamp(forecast['dt']).strftime('%a'),
                'temp': round(forecast['main']['temp']),
                'humidity': forecast['main']['humidity'],
                'rain_chance': forecast.get('pop', 0) * 100,  # Probability of precipitation
                'description': forecast['weather'][0]['description'],
                'wind_speed': forecast['wind']['speed'],
                'icon': forecast['weather'][0]['icon']
            })
        
        return {
            'city': city_name,
            'current_temp': round(current_weather['main']['temp']),
            'current_humidity': current_weather['main']['humidity'],
            'current_description': current_weather['weather'][0]['description'],
            'current_wind': current_weather['wind']['speed'],
            'current_icon': current_weather['weather'][0]['icon'],
            'forecast': forecast_data,
            'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        
    except Exception as e:
        st.error(f"Error fetching weather data: {e}")
        return get_mock_weather_data(city_name)

def get_mock_weather_data(city_name):
    """Generate mock weather data for demonstration purposes"""
    # Different weather patterns based on city
    if city_name.lower() in ["chennai", "madras"]:
        base_temp = 32
        rain_chance = 60
        wind_speed = 12
    elif city_name.lower() in ["mumbai", "bombay"]:
        base_temp = 30
        rain_chance = 70
        wind_speed = 15
    elif city_name.lower() in ["delhi", "new delhi"]:
        base_temp = 28
        rain_chance = 20
        wind_speed = 10
    elif city_name.lower() in ["bangalore", "bengaluru"]:
        base_temp = 26
        rain_chance = 40
        wind_speed = 8
    elif city_name.lower() in ["jorethang", "gangtok", "darjeeling"]:
        base_temp = 20
        rain_chance = 80
        wind_speed = 18
    else:
        base_temp = 28
        rain_chance = 50
        wind_speed = 10
    
    # Generate forecast data
    days = ["Today", "Mon", "Tue", "Wed", "Thu"]
    forecast_data = []
    
    for i, day in enumerate(days):
        temp_variation = np.random.randint(-3, 4)
        rain_variation = np.random.randint(-20, 21)
        wind_variation = np.random.randint(-5, 6)
        
        forecast_data.append({
            'day': day,
            'temp': base_temp + temp_variation,
            'humidity': 60 + np.random.randint(-15, 16),
            'rain_chance': max(0, min(100, rain_chance + rain_variation)),
            'wind_speed': max(0, wind_speed + wind_variation),
            'description': 'Partly cloudy',
            'icon': '02d' if rain_chance < 50 else '10d'
        })
    
    return {
        'city': city_name,
        'current_temp': forecast_data[0]['temp'],
        'current_humidity': forecast_data[0]['humidity'],
        'current_description': forecast_data[0]['description'],
        'current_wind': forecast_data[0]['wind_speed'],
        'current_icon': '02d',
        'forecast': forecast_data,
        'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }

# Market Price API Integration
def get_market_prices():
    """
    Fetch real-time market prices from API
    In a real implementation, this would connect to a market data API
    """
    try:
        # This is a placeholder for actual API integration
        # For demo purposes, we'll use mock data that changes slightly each time
        
        crops = ["Rice", "Wheat", "Tomato", "Potato", "Maize", "Sugarcane"]
        base_prices = [40, 30, 25, 20, 22, 15]
        
        market_data = []
        for i, crop in enumerate(crops):
            # Simulate small price fluctuations
            price_change = np.random.uniform(-2, 2)
            new_price = max(5, base_prices[i] + price_change)
            
            # Determine trend
            if price_change > 0.5:
                trend = "↑"
                trend_class = "market-up"
            elif price_change < -0.5:
                trend = "↓"
                trend_class = "market-down"
            else:
                trend = "→"
                trend_class = "market-same"
                
            market_data.append({
                "Crop": crop,
                "Price (₹/kg)": round(new_price, 1),
                "Trend": trend,
                "TrendClass": trend_class
            })
            
        return {
            "data": market_data,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        
    except Exception as e:
        st.error(f"Error fetching market data: {e}")
        # Return default data if API fails
        return {
            "data": [
                {"Crop": "Rice", "Price (₹/kg)": 40, "Trend": "→", "TrendClass": "market-same"},
                {"Crop": "Wheat", "Price (₹/kg)": 30, "Trend": "→", "TrendClass": "market-same"},
                {"Crop": "Tomato", "Price (₹/kg)": 25, "Trend": "→", "TrendClass": "market-same"},
                {"Crop": "Potato", "Price (₹/kg)": 20, "Trend": "→", "TrendClass": "market-same"},
                {"Crop": "Maize", "Price (₹/kg)": 22, "Trend": "→", "TrendClass": "market-same"},
                {"Crop": "Sugarcane", "Price (₹/kg)": 15, "Trend": "→", "TrendClass": "market-same"}
            ],
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }

# Crop database with information for multiple crops
crop_database = {
    "Rice": {
        "soil_type": "Clayey loam",
        "season": "Kharif (June-October)",
        "water_requirements": "High",
        "ph_range": "5.0-6.5",
        "common_pests": "Stem borer, Brown plant hopper",
        "hi": {
            "soil_type": "चिकनी दोमट मिट्टी",
            "season": "खरीफ (जून-अक्टूबर)",
            "water_requirements": "उच्च",
            "ph_range": "5.0-6.5",
            "common_pests": "तना छेदक, भूरा प्लांट हॉपर"
        },
        "pa": {
            "soil_type": "ਚਿਕੀ ਦੋਮਟ ਮਿੱਟੀ",
            "season": "ਖਰੀਫ (ਜੂਨ-ਅਕਤੂਬਰ)",
            "water_requirements": "ਉੱਚ",
            "ph_range": "5.0-6.5",
            "common_pests": "ਤਣਾ ਬੋरर, ਬ੍ਰਾਊਨ ਪਲਾਂਟ ਹੌਪਰ"
        }
    },
    "Wheat": {
        "soil_type": "Well-drained loamy soil",
        "season": "Rabi (November-April)",
        "water_requirements": "Medium",
        "ph_range": "6.0-7.5",
        "common_pests": "Aphids, Armyworm",
        "hi": {
            "soil_type": "अच्छी जल निकासी वाली दोमट मिट्टी",
            "season": "रबी (नवंबर-अप्रैल)",
            "water_requirements": "मध्यम",
            "ph_range": "6.0-7.5",
            "common_pests": "एफिड्स, आर्मीवर्म"
        },
        "pa": {
            "soil_type": "ਚੰਗੀ ਤਰ੍ਹਾਂ ਨਾਲ ਸੁੱਕੀ ਦੋਮਟ ਮਿੱਟੀ",
            "season": "ਰਬੀ (ਨਵੰਬर-ਅਪ੍ਰੈਲ)",
            "water_requirements": "ਦਰਮਿਆਨਾ",
            "ph_range": "6.0-7.5",
            "common_pests": "ਐਫਿਡ, ਆਰਮੀਵਰਮ"
        }
    },
    "Tomato": {
        "soil_type": "Well-drained sandy loam",
        "season": "Year-round with irrigation",
        "water_requirements": "Medium",
        "ph_range": "6.0-6.8",
        "common_pests": "Whiteflies, Tomato fruit borer",
        "hi": {
            "soil_type": "अच्छी जल निकासी वाली बलुई दोमट मिट्टी",
            "season": "सिंचाई के साथ साल भर",
            "water_requirements": "मध्यम",
            "ph_range": "6.0-6.8",
            "common_pests": "व्हाइटफ्लाइज़, टमाटर फल बोरर"
        },
        "pa": {
            "soil_type": "ਚੰਗी ਤਰ੍ਹਾਂ ਨਾਲ ਸੁੱਕੀ ਰੇਤਲੀ ਦੋमਟ ਮਿੱਟੀ",
            "season": "ਸਿੰਜਾਈ ਨਾਲ ਸਾਲ ਭਰ",
            "water_requirements": "ਦਰਮਿਆਨਾ",
            "ph_range": "6.0-6.8",
            "common_pests": "ਵ੍ਹਾਈਟਫਲਾਈਜ਼, ਟਮਾਟਰ ਫਲ ਬੋरਰ"
        }
    },
    "Potato": {
        "soil_type": "Well-drained sandy loam",
        "season": "Rabi (October-March)",
        "water_requirements": "Medium",
        "ph_range": "5.0-6.5",
        "common_pests": "Colorado potato beetle, Aphids",
        "hi": {
            "soil_type": "अच्छी जल निकासी वाली बलुई दोमट मिट्टी",
            "season": "रबी (अक्टूबर-मार्च)",
            "water_requirements": "मध्यम",
            "ph_range": "5.0-6.5",
            "common_pests": "कोलोराडो आलू बीटल, एफिड्स"
        },
        "pa": {
            "soil_type": "ਚੰਗੀ ਤਰ੍ਹਾਂ ਨਾਲ ਸੁੱਕੀ ਰੇਤਲੀ ਦੋਮਟ ਮਿੱਟੀ",
            "season": "ਰਬੀ (ਅਕਤੂਬर-ਮਾਰਚ)",
            "water_requirements": "ਦਰਮਿਆਨਾ",
            "ph_range": "5.0-6.5",
            "common_pests": "ਕੋਲੋਰਾਡੋ ਆਲੂ ਬੀਟਲ, ਐਫਿਡ"
        }
    },
    "Maize": {
        "soil_type": "Well-drained loamy soil",
        "season": "Kharif (June-September)",
        "water_requirements": "Medium",
        "ph_range": "5.5-7.0",
        "common_pests": "Stem borer, Armyworm",
        "hi": {
            "soil_type": "अच्छी जल निकासी वाली दोमट मिट्टी",
            "season": "खरीफ (जून-सितंबर)",
            "water_requirements": "मध्यम",
            "ph_range": "5.5-7.0",
            "common_pests": "तना छेदक, आर्मीवर्म"
        },
        "pa": {
            "soil_type": "ਚੰਗੀ ਤਰ੍ਹਾਂ ਨਾਲ ਸੁੱਕੀ ਦੋਮਟ ਮਿੱਟੀ",
            "season": "ਖਰੀਫ (ਜੂਨ-ਸਤੰਬਰ)",
            "water_requirements": "ਦਰਮਿਆਨਾ",
            "ph_range": "5.5-7.0",
            "common_pests": "ਤਣਾ ਬੋरर, ਆਰਮੀਵਰਮ"
        }
    },
    "Sugarcane": {
        "soil_type": "Deep rich loamy soil",
        "season": "Year-round with irrigation",
        "water_requirements": "High",
        "ph_range": "6.0-7.5",
        "common_pests": "Top borer, Scale insects",
        "hi": {
            "soil_type": "गहरी उपजाऊ दोमट मिट्टी",
            "season": "सिंचाई के साथ साल भर",
            "water_requirements": "उच्च",
            "ph_range": "6.0-7.5",
            "common_pests": "टॉप बोरर, स्केल कीट"
        },
        "pa": {
            "soil_type": "ਡੂੰਘੀ ਅਮੀਰ ਦੋਮਟ ਮਿੱਟੀ",
            "season": "ਸਿੰਜਾਈ ਨਾਲ ਸਾਲ ਭਰ",
            "water_requirements": "ਉੱਚ",
            "ph_range": "6.0-7.5",
            "common_pests": "ਟਾਪ ਬੋਰਰ, ਸਕੇਲ ਕੀੜੇ"
        }
    }
}

# Disease database with information for multiple crops
disease_database = {
    "Tomato": {
        "Early Blight": {
            "symptoms": "Dark spots with concentric rings on leaves, stems and fruits",
            "treatment": "Apply chlorothalonil or copper-based fungicides",
            "prevention": "Rotate crops, remove infected plants, ensure good air circulation",
            "hi": {
                "symptoms": "पत्तियों, तनों और फलों पर केंद्रित छल्ले वाले काले धब्बे",
                "treatment": "क्लोरोथालोनिल या तांबे आधारित कवकनाशी लगाएं",
                "prevention": "फसलों का रोटेशन, संक्रमित पौधों को हटाना, अच्छा वायु संचार सुनिश्चित करना"
            },
            "pa": {
                "symptoms": "ਪੱਤੀਆਂ, ਡੰਡੀਆਂ ਅਤੇ ਫਲਾਂ 'ਤੇ ਕੇਂਦਰਿਤ ਰਿੰਗਾਂ ਵਾਲੇ ਡਾਰਕ ਧੱਬੇ",
                "treatment": "ਕਲੋਰੋਥਾਲੋਨਿਲ ਜਾਂ ਤਾਂਬੇ-ਅਧਾਰਤ ਫੰਗੀਸਾਈਡਸ ਲਗਾਓ",
                "prevention": "ਫਸਲਾਂ ਦੀ ਘੁੰਮਾਓ, ਸੰਕਰਮਿਤ ਪੌਦਿਆਂ ਨੂੰ ਹਟਾਓ, ਚੰਗੀ ਹਵਾ ਪ੍ਰਣਾਲੀ ਨੂੰ ਯਕੀਨੀ ਬਣਾਓ"
            }
        },
        "Late Blight": {
            "symptoms": "Water-soaked lesions that turn brown and papery",
            "treatment": "Apply fungicides containing mancozeb or metalaxyl",
            "prevention": "Avoid overhead watering, remove volunteer plants",
            "hi": {
                "symptoms": "पानी से लथपथ घाव जो भूरे और कागजी हो जाते हैं",
                "treatment": "मैंकोजेब या मेटालाक्सिल युक्त कवकनाशी लगाएं",
                "prevention": "ओवरहेड वाटरिंग से बचें, स्वयंसेवक पौधों को हटा दें"
            },
            "pa": {
                "symptoms": "ਪਾਣੀ ਨਾਲ ਭਿੱਜੇ ਘਾਉ ਜੋ ਭੂਰੇ ਅਤੇ ਕਾਗਜ਼ੀ ਹੋ ਜਾਂਦੇ ਹਨ",
                "treatment": "ਮੈਨਕੋਜ਼ੇਬ ਜਾਂ ਮੈਟਾਲਾਕਸੀਲ ਯੁਕਤ ਫੰਗੀਸਾਈਡਸ ਲਗਾਓ",
                "prevention": "ਓਓਵਰਹੈਡ ਵਾਟਰਿੰਗ ਤੋਂ ਬਚੋ, ਰੁੱਖੇ ਪੌਦੇ ਹਟਾਓ"
            }
        }
    },
    "Potato": {
        "Late Blight": {
            "symptoms": "Dark, water-soaked spots on leaves with white mold under wet conditions",
            "treatment": "Apply fungicides containing chlorothalonil or mancozeb",
            "prevention": "Plant resistant varieties, avoid overhead irrigation",
            "hi": {
                "symptoms": "गीली परिस्थितियों में सफेद मोल्ड के साथ पत्तियों पर काले, पानी से लथपथ धब्बे",
                "treatment": "क्लोरोथालोनिल या मैंकोजेब युक्त कवकनाशी लगाएं",
                "prevention": "प्रतिरोधी किस्में लगाएं, ओवरहेड सिंचाई से बचें"
            },
            "pa": {
                "symptoms": "ਗਿੱਲੀ ਹਾਲਤ ਵਿੱਚ ਚਿੱਟੇ ਮੋਲਡ ਨਾਲ ਪੱਤੀਆਂ 'ਤੇ ਡਾਰ크, ਪਾਣੀ ਨਾਲ ਭਿੱਜੇ ਧੱਬੇ",
                "treatment": "ਕਲੋਰੋਥਾਲੋਨਿਲ ਜਾਂ ਮੈਨਕੋਜ਼ੇਬ ਯੁਕਤ ਫੰਗੀਸਾਈਡਸ ਲਗਾਓ",
                "prevention": "ਪ੍ਰਤੀਰੋਧਕ ਕਿਸਮਾਂ ਲਗਾਓ, ਓਵਰਹੈਡ ਸਿੰਜਾਈ ਤੋਂ ਬਚੋ"
            }
        }
    },
    "Rice": {
        "Blast": {
            "symptoms": "Spindle-shaped lesions with gray centers and brown margins",
            "treatment": "Apply fungicides containing tricyclazole or azoxystrobin",
            "prevention": "Use resistant varieties, avoid excessive nitrogen fertilization",
            "hi": {
                "symptoms": "ग्रे सेंटर और भूरे मार्जिन के साथ स्पिंडल के आकार के घाव",
                "treatment": "ट्राइसाइक्लाजोल या एज़ोक्सिस्ट्रोबिन युक्त कवकनाशी लगाएं",
                "prevention": "प्रतिरोधी किस्मों का उपयोग करें, अत्यधिक नाइट्रोजन निषेचन से बचें"
            },
            "pa": {
                "symptoms": "ਸਲੇਟੀ ਸੈਂਟਰ ਅਤੇ ਭੂਰੇ ਮਾਰਜਿਨ ਨਾਲ ਸਪਿੰਡਲ-ਆਕਾਰ ਦੇ ਘਾਉ",
                "treatment": "ਟ੍ਰਾਈਸਾਈਕਲਾਜ਼ੋਲ ਜਾਂ ਅਜ਼ੋਕਸੀਸਟ੍ਰੋਬਿਨ ਯੁਕਤ ਫੰਗੀਸਾਈਡਸ ਲਗਾਓ",
                "prevention": "ਪ੍ਰਤੀਰੋਧਕ ਕਿਸਮਾਂ ਦੀ ਵਰਤੋਂ ਕਰੋ, ਜ਼ਿਆਦਾ ਨਾਈਟ੍ਰੋਜਨ ਖਾਦ ਤੋਂ ਬਚੋ"
            }
        }
    }
}

# Indian cities with coordinates for weather data
indian_cities = [
    "Jorethang", "Gangtok", "Darjeeling", "Kolkata", "Mumbai", "Delhi", "Chennai", 
    "Bangalore", "Hyderabad", "Pune", "Ahmedabad", "Jaipur", "Lucknow", "Bhopal",
    "Patna", "Chandigarh", "Dehradun", "Shimla", "Agartala", "Guwahati", "Dispur"
]

# Function to process farmer queries
def process_farmer_query(query, lang_code="en"):
    """
    A simple rule-based function to process farmer queries.
    This is a basic example. A real system would use a proper NLP library.
    """
    query_lower = query.lower()
    
    # Define keywords for intents and entities
    keywords = {
        'crops': ['tomato', 'potato', 'rice', 'wheat', 'maize', 'sugarcane', 'फसल', 'टमाटर', 'आलू', 'गेहूं', 'चावल', 'ਮਕੀ', 'ਗੰਨਾ', 'ਫਸਲ', 'ਟਮਾਟਰ', 'ਆਲੂ'],
        'symptoms': ['yellow', 'spot', 'wilting', 'hole', ' insect', 'pest', 'पीला', 'धब्बे', 'मुरझाना', 'कीट', 'ਕੀੜਾ', 'ਪੀਲਾ', 'ਧੱਬੇ', 'ਮੁਰਝਾਨਾ'],
        'intent_question': ['how', 'what', 'why', 'when', 'where', 'कैसे', 'क्या', 'क्यों', 'कब', 'ਕਿਵੇਂ', 'ਕੀ', 'ਕਿਉਂ', 'ਕਦੋਂ'],
        'intent_problem': ['problem', 'issue', 'wrong', 'help', 'समस्या', 'मदद', 'ਮੁਸ਼ਕਲ', 'ਸਮੱਸਿਆ', 'ਮਦਦ']
    }
    
    # Simple intent classification
    intent = "unknown"
    for word in keywords['intent_question']:
        if word in query_lower:
            intent = "question"
            break
    for word in keywords['intent_problem']:
        if word in query_lower:
            intent = "problem"
            break
            
    # Simple entity extraction
    detected_crops = []
    for crop in keywords['crops']:
        if crop in query_lower:
            detected_crops.append(crop)
            
    detected_symptoms = []
    for symptom in keywords['symptoms']:
        if symptom in query_lower:
            detected_symptoms.append(symptom)
    
    return {
        "intent": intent,
        "crops": detected_crops,
        "symptoms": detected_symptoms,
        "original_query": query
    }

# Main app
def main():
    # Initialize session state for data caching
    if 'weather_data' not in st.session_state:
        st.session_state.weather_data = None
    if 'market_data' not in st.session_state:
        st.session_state.market_data = None
    if 'last_refresh' not in st.session_state:
        st.session_state.last_refresh = None
    
    # Language selection at the top
    col1, col2, col3 = st.columns([3, 1, 1])
    with col1:
        st.markdown(f'<h1 class="main-header">{ui_text["en"]["title"]}</h1>', unsafe_allow_html=True)
        st.markdown(f'<p style="text-align: center; font-size: 1.2rem;">{ui_text["en"]["welcome"]}</p>', unsafe_allow_html=True)
    
    with col2:
        st.write("")  # spacer
    
    with col3:
        language = st.selectbox(
            ui_text["en"]["select_language"],
            ["English", "Hindi", "Punjabi"],
            key="lang_select"
        )
    
    lang_code = "en" if language == "English" else "hi" if language == "Hindi" else "pa"
    
    # Sidebar with user info
    with st.sidebar:
        st.header("Farmer Information")
        city = st.selectbox(
            ui_text[lang_code]["select_city"],
            indian_cities,
            index=indian_cities.index("Jorethang") if "Jorethang" in indian_cities else 0
        )
        
        selected_crop = st.selectbox(
            ui_text[lang_code]["select_crop"],
            list(crop_database.keys())
        )
        
        # Refresh data button
        if st.button(ui_text[lang_code]["refresh_data"], use_container_width=True):
            st.session_state.weather_data = None
            st.session_state.market_data = None
            st.session_state.last_refresh = datetime.now()
            st.rerun()
        
        if st.session_state.last_refresh:
            st.caption(f"{ui_text[lang_code]['last_updated']}: {st.session_state.last_refresh.strftime('%H:%M:%S')}")
        
        st.markdown("---")
        st.header(ui_text[lang_code]["expert_help"])
        phone = st.text_input(ui_text[lang_code]["phone_label"], placeholder="+91XXXXXXXXXX")
        question = st.text_area(ui_text[lang_code]["question_label"], placeholder=ui_text[lang_code]["feedback_placeholder"])
        if st.button(ui_text[lang_code]["submit_question"]):
            if phone and question:
                # Process the query
                analysis = process_farmer_query(question, lang_code)
                
                # Show the user what we understood
                st.write("**We understood:**")
                st.write(f"**Intent:** {analysis['intent']}")
                st.write(f"**Crops:** {', '.join(analysis['crops']) if analysis['crops'] else 'None detected'}")
                st.write(f"**Symptoms:** {', '.join(analysis['symptoms']) if analysis['symptoms'] else 'None detected'}")
                
                # Try to give an automated response if it's a common problem
                if analysis['crops'] and analysis['symptoms']:
                    crop = analysis['crops'][0]
                    if crop in disease_database:
                        st.info("**Based on your description, this might help:**")
                        # In a real system, you would match symptoms to diseases here
                        for disease, info in disease_database[crop].items():
                            st.write(f"**{disease}**")
                            if lang_code == "en":
                                st.write(f"Treatment: {info['treatment']}")
                            else:
                                st.write(f"उपचार: {info[lang_code]['treatment']}" if lang_code == 'hi' else f"ਇਲਾਜ: {info[lang_code]['treatment']}")
                            break # Just show the first one for demo
                
                st.success(ui_text[lang_code]["thank_you"])
            else:
                st.warning("Please provide both phone number and question")
    
    # Main content with tabs
    tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
        ui_text[lang_code]["disease_detection"],
        ui_text[lang_code]["crop_advisory"],
        ui_text[lang_code]["market_prices"],
        ui_text[lang_code]["weather_info"],
        ui_text[lang_code]["soil_health"],
        ui_text[lang_code]["expert_advice"]
    ])
    
    # Tab 1: Disease Detection
    with tab1:
        st.header(ui_text[lang_code]["disease_detection"])
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader(ui_text[lang_code]["take_picture"])
            st.camera_input("", key="camera_input")
            
            st.subheader(ui_text[lang_code]["upload_image"])
            uploaded_file = st.file_uploader("", type=["jpg", "jpeg", "png"], label_visibility="collapsed")
            
            if st.button(ui_text[lang_code]["analyze"], use_container_width=True):
                if uploaded_file is not None:
                    # Simulate disease detection
                    image = Image.open(uploaded_file)
                    st.image(image, caption="Uploaded Image", use_column_width=True)
                    
                    # For demo purposes, randomly select a disease
                    if selected_crop in disease_database:
                        diseases = list(disease_database[selected_crop].keys())
                        detected_disease = np.random.choice(diseases)
                        
                        st.subheader(ui_text[lang_code]["prediction_result"])
                        st.warning(detected_disease)
                        
                        st.subheader(ui_text[lang_code]["advice"])
                        if lang_code == "en":
                            st.info(disease_database[selected_crop][detected_disease]["treatment"])
                        else:
                            st.info(disease_database[selected_crop][detected_disease][lang_code]["treatment"])
                        
                        st.subheader(ui_text[lang_code]["prevention"])
                        if lang_code == "en":
                            st.info(disease_database[selected_crop][detected_disease]["prevention"])
                        else:
                            st.info(disease_database[selected_crop][detected_disease][lang_code]["prevention"])
                        
                        # Voice output button
                        if st.button(ui_text[lang_code]["voice_output"]):
                            advice_text = f"{selected_crop} disease detected: {detected_disease}. Treatment: {disease_database[selected_crop][detected_disease]['treatment']}. Prevention: {disease_database[selected_crop][detected_disease]['prevention']}"
                            speak_text(advice_text, lang_code)
                    else:
                        st.info("No diseases known for this crop or healthy plant detected")
                else:
                    st.warning("Please upload an image first")
        
        with col2:
            st.subheader("Common Diseases")
            if selected_crop in disease_database:
                for disease, info in disease_database[selected_crop].items():
                    with st.expander(disease):
                        if lang_code == "en":
                            st.write("**Symptoms:**", info["symptoms"])
                            st.write("**Treatment:**", info["treatment"])
                            st.write("**Prevention:**", info["prevention"])
                        else:
                            st.write("**लक्षण:**" if lang_code == "hi" else "**ਲੱਛਣ:**", info[lang_code]["symptoms"])
                            st.write("**उपचार:**" if lang_code == "hi" else "**ਇਲਾਜ:**", info[lang_code]["treatment"])
                            st.write("**रोकथाम:**" if lang_code == "hi" else "**ਰੋਕਥਾਮ:**", info[lang_code]["prevention"])
            else:
                st.info("No disease information available for this crop")
    
    # Tab 2: Crop Advisory
    with tab2:
        st.header(ui_text[lang_code]["crop_advisory"])
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader(f"{selected_crop} {ui_text[lang_code]['best_season']}")
            if lang_code == "en":
                st.info(crop_database[selected_crop]["season"])
            else:
                st.info(crop_database[selected_crop][lang_code]["season"])
            
            st.subheader(ui_text[lang_code]["soil_type"])
            if lang_code == "en":
                st.info(crop_database[selected_crop]["soil_type"])
            else:
                st.info(crop_database[selected_crop][lang_code]["soil_type"])
            
            st.subheader(ui_text[lang_code]["water_needs"])
            if lang_code == "en":
                st.info(crop_database[selected_crop]["water_requirements"])
            else:
                st.info(crop_database[selected_crop][lang_code]["water_requirements"])
        
        with col2:
            st.subheader(ui_text[lang_code]["ph_level"])
            if lang_code == "en":
                st.info(crop_database[selected_crop]["ph_range"])
            else:
                st.info(crop_database[selected_crop][lang_code]["ph_range"])
            
            st.subheader(ui_text[lang_code]["common_pests"])
            if lang_code == "en":
                st.info(crop_database[selected_crop]["common_pests"])
            else:
                st.info(crop_database[selected_crop][lang_code]["common_pests"])
            
            # Fertilizer recommendation
            st.subheader("Fertilizer Recommendation" if lang_code == "en" else "उर्वरक सिफारिश" if lang_code == "hi" else "ਖਾਦ ਸਿਫਾਰਿਸ਼")
            if selected_crop == "Rice":
                st.info("N:P:K - 100:50:50 kg/ha" if lang_code == "en" else "N:P:K - 100:50:50 kg/हेक्टेयर")
            elif selected_crop == "Wheat":
                st.info("N:P:K - 120:60:40 kg/ha" if lang_code == "en" else "N:P:K - 120:60:40 kg/हेक्टेयर")
            elif selected_crop == "Tomato":
                st.info("N:P:K - 150:100:100 kg/ha" if lang_code == "en" else "N:P:K - 150:100:100 kg/हेक्टेयर")
            else:
                st.info("N:P:K - 100:50:50 kg/ha" if lang_code == "en" else "N:P:K - 100:50:50 kg/हेक्टेयर")
        
        # Crop calendar
        st.subheader(ui_text[lang_code]["crop_calendar"])
        calendar_data = {
            "Month": ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"],
            "Activity": ["Planning", "Soil Prep", "Sowing", "Irrigation", "Weeding", "Fertilization", 
                         "Pest Control", "Harvest", "Post-Harvest", "Marketing", "Rest", "Planning"]
        }
        calendar_df = pd.DataFrame(calendar_data)
        st.dataframe(calendar_df, use_container_width=True)
    
    # Tab 3: Market Prices
    with tab3:
        st.header(ui_text[lang_code]["market_prices"])
        
        # Get market data (from cache or API)
        if st.session_state.market_data is None:
            with st.spinner("Fetching market data..."):
                st.session_state.market_data = get_market_prices()
        
        market_data = st.session_state.market_data
        
        # Display last updated time
        st.caption(f"{ui_text[lang_code]['last_updated']}: {market_data['timestamp']}")
        
        # Display market data
        st.subheader(ui_text[lang_code]["real_time_data"])
        
        # Create a formatted table with colored trends
        for item in market_data["data"]:
            col1, col2, col3 = st.columns([2, 1, 1])
            with col1:
                st.write(f"**{item['Crop']}**")
            with col2:
                st.write(f"₹{item['Price (₹/kg)']}/kg")
            with col3:
                st.markdown(f"<span class='{item['TrendClass']}'>**{item['Trend']}**</span>", unsafe_allow_html=True)
            st.progress(min(100, int(item['Price (₹/kg)'] * 2)))
        
        # Price trends chart
        st.subheader(ui_text[lang_code]["market_trends"])
        fig, ax = plt.subplots(figsize=(10, 5))
        crops = [item['Crop'] for item in market_data["data"]]
        prices = [item['Price (₹/kg)'] for item in market_data["data"]]
        colors = ['#4caf50' if '↑' in item['Trend'] else '#f44336' if '↓' in item['Trend'] else '#ff9800' for item in market_data["data"]]
        
        bars = ax.bar(crops, prices, color=colors)
        ax.set_ylabel('Price (₹/kg)')
        plt.xticks(rotation=45)
        
        # Add value labels on bars
        for bar, price in zip(bars, prices):
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height + 0.1,
                    f'₹{price}', ha='center', va='bottom')
        
        st.pyplot(fig)
        
        # Market analysis
        st.subheader(ui_text[lang_code]["market_analysis"])
        st.info("""
        Current market trends show increasing prices for vegetables due to seasonal demand. 
        Grain prices are stable with slight fluctuations. Consider diversifying your crops 
        to maximize profits during peak seasons.
        """)
    
    # Tab 4: Weather Info
    with tab4:
        st.header(ui_text[lang_code]["weather_info"])
        
        # Get weather data (from cache or API)
        if st.session_state.weather_data is None or st.session_state.weather_data['city'] != city:
            with st.spinner("Fetching weather data..."):
                st.session_state.weather_data = get_weather_data(city)
        
        weather_data = st.session_state.weather_data
        
        # Display last updated time
        st.caption(f"{ui_text[lang_code]['last_updated']}: {weather_data['timestamp']}")
        
        # Weather alerts - show different alerts based on weather conditions
        alert_message = None
        alert_class = "weather-alert"
        
        if weather_data['forecast'][0]['rain_chance'] > 70:
            alert_message = ui_text[lang_code]["rain_alert"]
            alert_class = "urgent-alert"
        elif weather_data['current_temp'] > 35:
            alert_message = ui_text[lang_code]["temp_alert"]
        elif weather_data['current_wind'] > 15:
            alert_message = ui_text[lang_code]["wind_alert"]
        
        if alert_message:
            st.markdown(f'<div class="{alert_class}">', unsafe_allow_html=True)
            st.subheader(ui_text[lang_code]["alert"])
            st.write(alert_message)
            st.markdown('</div>', unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Current weather
            st.subheader(f"{ui_text[lang_code]['weather_forecast']} - {weather_data['city']}")
            
            # Display current weather metrics
            col1a, col1b = st.columns(2)
            with col1a:
                st.metric("Temperature", f"{weather_data['current_temp']}°C")
                st.metric("Humidity", f"{weather_data['current_humidity']}%")
            
            with col1b:
                rain_chance = weather_data['forecast'][0]['rain_chance']
                st.metric("Rain Chance", f"{rain_chance}%")
                st.metric("Wind Speed", f"{weather_data['current_wind']} km/h")
            
            st.write(f"**Conditions:** {weather_data['current_description'].title()}")
    
        with col2:
            # 5-day forecast
            st.subheader("5-Day Forecast" if lang_code == "en" else "5-दिन का पूर्वानुमान" if lang_code == "hi" else "5-ਦਿਨ ਦਾ ਪੂਰਵਾਨੁਮਾਨ")
            
            # Create forecast dataframe
            forecast_df = pd.DataFrame(weather_data['forecast'])
            
            # Display as a table
            st.dataframe(
                forecast_df[['day', 'temp', 'rain_chance', 'wind_speed']].rename(columns={
                    'day': 'Day',
                    'temp': 'Temp (°C)',
                    'rain_chance': 'Rain (%)',
                    'wind_speed': 'Wind (km/h)'
                }),
                use_container_width=True
            )
        
        # Weather chart
        st.subheader("Detailed Forecast" if lang_code == "en" else "विस्तृत पूर्वानुमान" if lang_code == "hi" else "ਵਿਸਤ੍ਰਿਤ ਪੂਰਵਾਨੁਮਾਨ")
        fig, ax = plt.subplots(figsize=(10, 5))
        
        days = [f['day'] for f in weather_data['forecast']]
        temps = [f['temp'] for f in weather_data['forecast']]
        rain = [f['rain_chance'] for f in weather_data['forecast']]
        
        ax.plot(days, temps, marker='o', label='Temperature (°C)', linewidth=2.5)
        ax.set_ylabel('Temperature (°C)', color='red')
        ax.tick_params(axis='y', labelcolor='red')
        
        ax2 = ax.twinx()
        ax2.bar(days, rain, alpha=0.3, color='blue', label='Rain Chance (%)')
        ax2.set_ylabel('Rain Chance (%)', color='blue')
        ax2.tick_params(axis='y', labelcolor='blue')
        ax2.set_ylim(0, 100)
        
        ax.set_title('5-Day Weather Forecast')
        ax.legend(loc='upper left')
        ax2.legend(loc='upper right')
        
        st.pyplot(fig)
        
        # Weather warnings
        st.subheader(ui_text[lang_code]["weather_warnings"])
        if weather_data['forecast'][0]['rain_chance'] > 60:
            st.warning("Heavy rainfall expected. Consider delaying outdoor activities and protect crops from waterlogging.")
        if weather_data['current_temp'] > 33:
            st.warning("High temperatures may stress crops. Ensure adequate irrigation.")
        if weather_data['current_wind'] > 15:
            st.warning("Strong winds expected. Secure loose items and protect delicate plants.")
    
    # Tab 5: Soil Health
    with tab5:
        st.header(ui_text[lang_code]["soil_health"])
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader(ui_text[lang_code]["soil_tips"])
            tips = [
                "Test soil every season for nutrient levels",
                "Add organic compost to improve soil structure",
                "Practice crop rotation to maintain soil health",
                "Use cover crops to prevent erosion",
                "Maintain proper pH levels for your crops"
            ]
            
            if lang_code != "en":
                tips = [translate_text(tip, lang_code) for tip in tips]
                
            for tip in tips:
                st.write(f"• {tip}")
            
            # Soil testing information
            st.subheader("Soil Testing" if lang_code == "en" else "मृदा परीक्षण" if lang_code == "hi" else "ਮਿੱਟੀ ਟੈਸਟਿੰਗ")
            st.info("Contact your local agricultural office for soil testing services. Regular soil testing helps determine the right fertilizer composition for your farm.")
        
        with col2:
            # Soil health metrics
            st.subheader("Your Soil Health" if lang_code == "en" else "आपका मृदा स्वास्थ्य" if lang_code == "hi" else "ਤੁਹਾਡਾ ਮਿੱਟੀ ਦਾ ਸਿਹਤ")
            
            # pH level
            st.metric("pH Level", "6.2", "0.3")
            st.progress(0.62)
            
            # Organic matter
            st.metric("Organic Matter", "3.5%", "-0.2%")
            st.progress(0.35)
            
            # Nutrient levels
            st.metric("Nitrogen", "Medium", None)
            st.progress(0.5)
            
            st.metric("Phosphorus", "Low", None)
            st.progress(0.3)
            
            st.metric("Potassium", "High", None)
            st.progress(0.8)
            
            # Soil moisture based on weather
            if weather_data['forecast'][0]['rain_chance'] > 50:
                moisture_status = "Adequate"
                moisture_value = 0.7
            else:
                moisture_status = "Low"
                moisture_value = 0.3
                
            st.metric("Soil Moisture", moisture_status)
            st.progress(moisture_value)
    
    # Tab 6: Expert Advice and Community
    with tab6:
        st.header(ui_text[lang_code]["expert_advice"])
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Agricultural Tips")
            tips = [
                "Rotate crops to prevent soil depletion",
                "Use organic fertilizers for sustainable farming",
                "Implement drip irrigation to conserve water",
                "Monitor plants regularly for early pest detection",
                "Consider intercropping to maximize land use"
            ]
            
            if lang_code != "en":
                tips = [translate_text(tip, lang_code) for tip in tips]
                
            for tip in tips:
                st.write(f"• {tip}")
            
            # Government schemes
            st.subheader(ui_text[lang_code]["gov_schemes"])
            schemes = [
                "PM-KISAN: ₹6,000/year financial support",
                "Soil Health Card Scheme: Free soil testing",
                "National Mission on Sustainable Agriculture",
                "Pradhan Mantri Fasal Bima Yojana: Crop insurance"
            ]
            
            if lang_code != "en":
                schemes = [translate_text(scheme, lang_code) for scheme in schemes]
                
            for scheme in schemes:
                st.write(f"• {scheme}")
        
        with col2:
            st.subheader(ui_text[lang_code]["community_forum"])
            
            # Sample forum posts
            posts = [
                {"user": "Raju Kumar", "text": "Has anyone tried the new organic pesticide? Results?"},
                {"user": "Priya Singh", "text": "Looking for advice on tomato cultivation in rainy season"},
                {"user": "Amandeep Singh", "text": "Sharing my success with drip irrigation - 30% water saved!"},
                {"user": "Vikram Patel", "text": "Best time to harvest wheat in North India?"}
            ]
            
            for post in posts:
                with st.expander(f"{post['user']}: {post['text']}"):
                    st.write("**Comments:**")
                    st.write("- Great question! I've had good results with...")
                    st.write("- In my experience, the best time is...")
                    st.write("- Thanks for sharing this information!")
            
            # Add new post
            new_post = st.text_input("Add your question or comment:")
            if st.button("Post"):
                if new_post:
                    st.success("Your post has been added to the community forum!")
                else:
                    st.warning("Please enter some text for your post.")

if __name__ == "__main__":
    main()