from django.shortcuts import render, redirect, get_object_or_404
from datetime import datetime, timezone
from .api import get_weather_data, get_city_choices
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.contrib import messages
from .forms import CitySubscriptionForm, RegisterForm, CommentForm
from .models import CitySubscription, Comment
import random
import geonamescache

def main_page(request):
    gc = geonamescache.GeonamesCache()

    cities = gc.get_cities()

    city_names = [city['name'] for city in cities.values() if city['population'] > 1000000]

    # Select 12 random cities from the list
    random_cities = random.sample(city_names, min(len(city_names), 12))
    weather_reports = [get_weather_data(city) for city in random_cities]
    
    return render(request, 'weather_app/main_page.html', {
        'weather_reports': weather_reports,
    })



@login_required
def manage_subscriptions(request):
    if request.method == 'POST':
        form = CitySubscriptionForm(request.POST)
        if form.is_valid():
            city_name = form.cleaned_data['city_name']
            # Check if the user is already subscribed to this city
            if CitySubscription.objects.filter(user=request.user, city_name=city_name).exists():
                messages.error(request, f'You are already subscribed to {city_name}.')
            else:
                new_subscription = form.save(commit=False)
                new_subscription.user = request.user
                new_subscription.save()
                return redirect('manage_subscriptions')  # Refresh to see changes
    else:
        form = CitySubscriptionForm()
    
    subscriptions = CitySubscription.objects.filter(user=request.user)
    detailed_weather_reports = []
    for subscription in subscriptions:
        report = get_weather_data(subscription.city_name)
        
        # Convert UNIX timestamps to datetime objects
        sunrise_time = datetime.fromtimestamp(report['sys']['sunrise'], tz=timezone.utc)
        sunset_time = datetime.fromtimestamp(report['sys']['sunset'], tz=timezone.utc)
        
        # Add the converted times to the report dictionary
        report['formatted_sunrise'] = sunrise_time.strftime("%H:%M")
        report['formatted_sunset'] = sunset_time.strftime("%H:%M")
        detailed_weather_reports.append((subscription, report))

    return render(request, 'weather_app/manage_subscriptions.html', {
        'form': form,
        'detailed_weather_reports': detailed_weather_reports,
    })

def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('main_page')  # Redirect to a desired page
    else:
        form = RegisterForm()
    return render(request, 'weather_app/register.html', {'form': form})

@login_required
def unsubscribe(request, subscription_id):
    subscription = get_object_or_404(CitySubscription, id=subscription_id, user=request.user)
    if request.method == 'POST':
        subscription.delete()
        return redirect('manage_subscriptions')
    else:
        # how is it possible?!
        return redirect('manage_subscriptions')

@login_required
def city_detail(request, city_name):
    # Fetch the city subscription and weather data
    subscription = get_object_or_404(CitySubscription, user=request.user, city_name=city_name)
    weather_report = get_weather_data(city_name)

    if request.method == 'POST':
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.user = request.user
            new_comment.city_subscription = subscription
            new_comment.save()
            return redirect('city_detail', city_name=city_name)  # Reload
    else:
        comment_form = CommentForm()

    # Fetch existing comments for the city
    comments = Comment.objects.filter(city_subscription=subscription).order_by('-created_at')
    return render(request, 'weather_app/city_detail.html', {
        'subscription': subscription,
        'weather_report': weather_report,
        'comments': comments,
        'comment_form': comment_form,
    })

@login_required
def delete_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id, user=request.user)  
    city_name = comment.city_subscription.city_name
    comment.delete()
    return redirect('city_detail', city_name=city_name)


