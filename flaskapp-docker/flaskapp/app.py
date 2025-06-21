from flask import Flask, jsonify, request, Response
import requests
import time
from prometheus_client import Counter, Histogram, generate_latest, CONTENT_TYPE_LATEST

app = Flask(__name__)

# Prometheus metrics
REQUEST_COUNT = Counter(
    'weather_requests_total', 
    'Total number of requests to the weather endpoint', 
    ['method', 'endpoint', 'http_status']
)

REQUEST_LATENCY = Histogram(
    'weather_request_duration_seconds', 
    'Latency of weather endpoint', 
    ['endpoint']
)

@app.route('/weather', methods=['GET'])
def get_weather():
    start_time = time.time()
    endpoint = '/weather'

    city = request.args.get('city')
    if not city:
        REQUEST_COUNT.labels(method='GET', endpoint=endpoint, http_status='400').inc()
        return jsonify({'error': 'Missing city parameter'}), 400

    try:
        api_key = '3cd98018f5dc8e61267f3931b1cbff89'  # Replace with secret handling for prod
        openweathermap_api_url = (
            f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric'
        )
        response = requests.get(openweathermap_api_url)
        data = response.json()

        REQUEST_COUNT.labels(method='GET', endpoint=endpoint, http_status=str(response.status_code)).inc()
        REQUEST_LATENCY.labels(endpoint=endpoint).observe(time.time() - start_time)

        return jsonify({
            'temperature': data['main']['temp'],
            'humidity': data['main']['humidity'],
            'wind_speed': data['wind']['speed']
        })

    except Exception as e:
        REQUEST_COUNT.labels(method='GET', endpoint=endpoint, http_status='500').inc()
        return jsonify({'error': str(e)}), 500

@app.route('/metrics')
def metrics():
    return Response(generate_latest(), mimetype=CONTENT_TYPE_LATEST)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)  # Critical for Kubernetes and Docker
