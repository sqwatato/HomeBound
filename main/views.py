from django.shortcuts import render
from .models import Opportunity, Shelter
import os
from dotenv import load_dotenv
load_dotenv()
from geopy.geocoders import GoogleV3
from geopy import distance
from pprint import pprint
# Create your views here.
API_KEY = os.getenv('MAP_API')
geo = GoogleV3(api_key=API_KEY)

def geocode_address(geo_locator, line_address, component_restrictions=None, retry_counter=0):
    # the geopy GoogleV3 geocoding call
    location = geo_locator.geocode(line_address, components=component_restrictions)

    # build a dict to append to output CSV
    if location is not None:
        location_result = {"Lat": location.latitude, "Long": location.longitude, "Error": "",
                            "formatted_address": location.raw['formatted_address'],
                            "location_type": location.raw['geometry']['location_type']}
    return location_result

def index(request):
    return render(request, 'index.html', {
        'opportunities': Opportunity.objects.filter(urgent=True),
    })

def catalog(request):
    context = {
        'opportunities': Opportunity.objects.all(),
        'count': Opportunity.objects.count(),
    }
    if request.method == 'POST':
        location = request.POST['location']
        d = int(request.POST.get('distance'))
        end = []
        lat, lon = geo.geocode(location)[1]
        for op in Opportunity.objects.all():
            if op.shelter.lat and op.shelter.lon:
                if distance.distance((lat, lon), (op.shelter.lat, op.shelter.lon)).miles <= d:
                    end.append(op)
        
        context = {
            'opportunities': end,
            'count': len(end)
        }
    return render(request, 'catalog.html', context)

def species(request, species):
    if request.method == 'POST':
        tmp = Opportunity.objects.all()
        if species.lower() == 'other':
            tmp = tmp.exclude(species__iexact='Dog').exclude(species__iexact='Cat')
        else:
            tmp = tmp.filter(species__iexact=species)
        location = request.POST['location']
        d = int(request.POST.get('distance'))
        end = []
        lat, lon = geo.geocode(location)[1]
        for op in tmp:
            if op.shelter.lat and op.shelter.lon:
                if distance.distance((lat, lon), (op.shelter.lat, op.shelter.lon)).miles <= d:
                    end.append(op)
        
        return render(request, 'catalog.html', {
            'opportunities': end,
            'count': len(end)
        })

        
    if species.lower() == 'other':
        return render(request, 'catalog.html', {
            'opportunities': Opportunity.objects.exclude(species__iexact='Dog').exclude(species__iexact='Cat'),
            'count': Opportunity.objects.exclude(species__iexact='Dog').exclude(species__iexact='Cat').count(),
        })
    return render(request, 'catalog.html', {
        'opportunities': Opportunity.objects.filter(species__iexact=species),
        'count': Opportunity.objects.filter(species__iexact=species).count(),
    })


def post(request):
    return render(request, 'post.html')