# app.py
from flask import Flask, jsonify, request
import requests
from prometheus_client import start_http_server, Summary, Counter

app = Flask(__name__)

# Prometheus metrics
REQUEST_COUNT = Counter('weather_api_requests_total', 'Total number of weather API requests')
REQUEST_LATENCY = Summary('weather_api_request_latency_seconds', 'Latency of weather API requests')

@app.route('/weather', methods=['GET'])
@REQUEST_LATENCY.time()
def get_weather():
    REQUEST_COUNT.inc()

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
    # Start Prometheus metrics server on port 8000
    start_http_server(8000)
    app.run(host='0.0.0.0', port=5000, debug=True)
