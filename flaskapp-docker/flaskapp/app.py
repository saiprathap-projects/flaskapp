# app.py
from flask import Flask, jsonify, request
import requests

app = Flask(__name__)

@app.route('/weather', methods=['GET'])
def get_weather():
    city = request.args.get('city')
    if not city:
        return jsonify({'error': 'Missing city parameter'}), 400

    api_key = '3cd98018f5dc8e61267f3931b1cbff89'  # Replace with your API key
    openweathermap_api_url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric'
    response = requests.get(openweathermap_api_url)
    data = response.json()

    return jsonify({
        'temperature': data['main']['temp'],
        'humidity': data['main']['humidity'],
        'wind_speed': data['wind']['speed']
    })

if __name__ == '__main__':
    app.run(debug=True)
