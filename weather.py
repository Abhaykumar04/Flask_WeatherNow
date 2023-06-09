from flask import Flask, render_template, request
import requests
from markupsafe import escape
import gunicorn

app = Flask(__name__,template_folder='templates')

@app.route('/', methods=['GET', 'POST'])
def weather():
    if request.method == 'POST':
        city = request.form['city']
        api_key = '5a8af2c4d9ee50a08c8d0d9ef2d8e920'  # Replace with your actual API key

        # Make a request to the weather API
        url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}'
        response = requests.get(url)
        data = response.json()

        if data['cod'] == '404':
            error_message = f"Weather information for '{city}' not found."
            return render_template('weather.html', error_message=error_message)

        # Extract relevant weather information from the API response
        weather_description = data['weather'][0]['description'].capitalize()
        temperature = data['main']['temp']
        humidity = data['main']['humidity']
        wind_speed = data['wind']['speed']

        # Convert temperature to Celsius
        temperature = round(temperature - 273.15, 2)

        return render_template('weather.html', city=city, weather_description=weather_description,
                               temperature=temperature, humidity=humidity, wind_speed=wind_speed)

    return render_template('weather.html')

if __name__ == '__main__':
    app.run(debug=True)

