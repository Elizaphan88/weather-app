import os
from django.shortcuts import render
import requests

def index(request):
    data = {}
    
    if request.method == 'POST':
        city = request.POST.get('city')
        
        if city:
            try:
                api_key = os.environ.get('OPENWEATHER_API_KEY', 'd853353733fcf955d742dfb9f19036bf')
                url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}'
                response = requests.get(url)
                list_of_data = response.json()
                
                if response.status_code == 200:
                    temp_celsius = list_of_data['main']['temp'] - 273.15

                    data = {
                        "country_code": str(list_of_data['sys']['country']),
                        "coordinate": f"{list_of_data['coord']['lon']}, {list_of_data['coord']['lat']}",
                        "temp": f"{temp_celsius:.2f} °C",
                        "pressure": str(list_of_data['main']['pressure']),
                        "humidity": str(list_of_data['main']['humidity']),
                        "main": str(list_of_data['weather'][0]['main']),
                        "description": str(list_of_data['weather'][0]['description']),
                        "icon": list_of_data['weather'][0]['icon'],
                    }
                else:
                    data = {"error": "City not found or invalid API response."}
                    
            except requests.exceptions.RequestException as e:
                data = {"error": "Network error occurred. Please try again."}
                print(f"Error occurred: {e}")
        else:
            data = {"error": "Please enter a valid city."}
    
    return render(request, "index.html", data)
