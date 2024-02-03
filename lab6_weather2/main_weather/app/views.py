from django.shortcuts import render, redirect, get_object_or_404
from .utils import get_weather_data_for_cities, get_forecast_data_for_city, get_detailed_weather_data, get_lon_lat_data
from collections import defaultdict
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views import generic
from .models import Location, Subscription, Observation
from django.contrib.auth.decorators import login_required
from .forms import ObservationForm
from django.contrib import messages

def homepage(request):
    
    cities = ["Moscow", "New York", "Kiev", "Cheboksary"]
    weather_data = get_weather_data_for_cities(cities)
    subscribed_cities = []
    if request.user.is_authenticated:
        subscribed_cities = Subscription.objects.filter(user=request.user).select_related('location')
        
    sub_cities = []
    if len(subscribed_cities) != 0:
        for sub in subscribed_cities:
            sub_cities.append(sub.location.name)
    sub_weather_data = get_weather_data_for_cities(sub_cities)

    context = {
        'weather_data': weather_data,
        'sub_weather_data': sub_weather_data,
        'subscribed_cities': subscribed_cities,
    }

    return render(request, 'app/homepage.html', context)


def search_weather(request):
    query = request.GET.get('location', '') 
    if query:
        weather_data = get_weather_data_for_cities([query])
    else:
        weather_data = []

    context = {'weather_data': weather_data, 'query': query}
    
    return render(request, 'app/search_results.html', context)


def weather_details(request, city_name):
    try:
        city = Location.objects.get(name=city_name)
        if request.user.is_authenticated:
            is_subscribed = Subscription.objects.filter(user=request.user, location=city).exists()
        else:
            is_subscribed = False
    except Location.DoesNotExist:
        city = None
        is_subscribed = False
    observations = Observation.objects.filter(location=city).order_by('-date_of_review')

    context = {
        'weather_data': get_detailed_weather_data(city_name),
        'is_subscribed': is_subscribed,
        'city': city_name,
        'city_id': city.id if city is not None else None,
        'observations': observations,
    }
    return render(request, 'app/weather_details.html', context)


def weather_forecast(request, city_name):
    raw_forecast_data = get_forecast_data_for_city(city_name)
    forecast_data_by_day = defaultdict(list)
    for item in raw_forecast_data:
        day = item['datetime'].split(' ')[0]  # 'datetime' like '2024-02-03 12:00:00'
        forecast_data_by_day[day].append(item)

    context = {
        'city_name': city_name,
        'forecast_data': dict(forecast_data_by_day),
    }
    return render(request, 'app/weather_forecast.html', context)


@login_required
def subscribe_to_city(request, city_name):
    # Check if the city already exists
    location, created = Location.objects.get_or_create(
        name=city_name,
        defaults={'latitude': None, 'longitude': None}
    )

    if created:
        # Fetch from API call
        response = get_lon_lat_data(city_name)
        location.latitude = response['lat']
        location.longitude = response['lon']
        location.save()

    Subscription.objects.get_or_create(user=request.user, location=location)

    return redirect('homepage')


@login_required
def unsubscribe_from_city(request, city_name):
    city = get_object_or_404(Location, name=city_name)
    
    Subscription.objects.filter(user=request.user, location=city).delete()

    return redirect('homepage')  # Redirect user after the operation

class SignUpView(generic.CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'registration/signup.html'


# Observations

@login_required
def add_observation(request, location_id):
    location = get_object_or_404(Location, id=location_id)
    # Check if the user is subscribed to the city
    if not Subscription.objects.filter(user=request.user, location=location).exists():
        messages.error(request, "You must be subscribed to this city to add observations.")
        return redirect('weather_details', city_name=location.name)
    
    if request.method == 'POST':
        form = ObservationForm(request.POST, request.FILES)
        if form.is_valid():
            observation = form.save(commit=False)
            observation.user = request.user
            observation.location = location
            observation.save()
            messages.success(request, "Observation added successfully.")
            return redirect('weather_details', city_name=location.name)
    else:
        form = ObservationForm()
    
    return render(request, 'app/add_observation.html', {'form': form, 'location': location})

@login_required
def edit_observation(request, observation_id):
    observation = get_object_or_404(Observation, id=observation_id, user=request.user)
    if request.method == 'POST':
        form = ObservationForm(request.POST, request.FILES, instance=observation)
        if form.is_valid():
            form.save()
            return redirect('weather_details', city_name=observation.location.name)
    else:
        form = ObservationForm(instance=observation)
    return render(request, 'app/edit_observation.html', {'form': form, 'observation': observation})

@login_required
def delete_observation(request, observation_id):
    observation = get_object_or_404(Observation, id=observation_id, user=request.user)
    if request.method == 'POST':
        observation.delete()
        return redirect('weather_details', city_name=observation.location.name)
    return render(request, 'app/delete_observation.html', {'observation': observation})

