from django.shortcuts import render

from django.contrib import messages
import requests
import datetime

def home(request):
    # Default city if not provided in POST request
    city = request.POST.get('city', 'indore')
    
    # OpenWeatherMap API details
    weather_api_key = 'YOUR_OPENWEATHERMAP_API_KEY'
    weather_url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid=eeed8df776b87a91f27bf92ae23aa312"
    weather_params = {'units': 'metric'}
    
    # Google Custom Search API details
    search_engine_id = '673629e27332045d2'
    google_api_key = 'AIzaSyAkDjYf5UUtKJdqwltlG8fcucP_RUqT2yg'
    query = f'{city} 1920x1080'
    page = 1
    start = (page - 1) * 10 + 1
    search_type = 'image'
    image_search_url = f"https://www.googleapis.com/customsearch/v1?key={google_api_key}&cx={search_engine_id}&q={query}&start={start}&searchType={search_type}&imgSize=xlarge"
    
    try:
        # Fetch weather data from OpenWeatherMap API
        weather_response = requests.get(weather_url, params=weather_params)
        weather_data = weather_response.json()
        
        # Extract relevant weather information
        description = weather_data['weather'][0]['description']
        icon = weather_data['weather'][0]['icon']
        temp = weather_data['main']['temp']
        day = datetime.date.today()
        
     #    # Fetch image URL from Google Custom Search API
        image_response = requests.get(image_search_url)
        image_data = image_response.json()
        image_url = image_data['items'][0]['link']  # Assuming the first image link
        
        return render(request, 'index.html', {
            'description': description,
            'icon': icon,
            'temp': temp,
            'day': day,
            'city': city,
            'exception_occurred': False,
            'image_url': image_url
        })
    
    except requests.exceptions.RequestException as e:
        # Handle API request errors
        exception_occurred = True
        messages.error(request, f'Error fetching data: {str(e)}')
        return render(request, 'index.html', {
            'description': 'Clear sky',  # Default values in case of error
            'icon': '01d',
            'temp': 25,
            'day': datetime.date.today(),
            'city': city,
            'exception_occurred': exception_occurred,
            'image_url': ''
        })
    
    except KeyError as e:
        # Handle missing data keys in API response
        exception_occurred = True
        messages.error(request, f'Data key error: {str(e)}')
        return render(request, 'index.html', {
            'description': 'Clear sky',  # Default values in case of error
            'icon': '01d',
            'temp': 25,
            'day': datetime.date.today(),
            'city': city,
            'exception_occurred': exception_occurred,
            'image_url': ''
        })
