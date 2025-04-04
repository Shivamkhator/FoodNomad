from django.shortcuts import render
import requests
import time
import math
from django.http import JsonResponse

def home(request):
    return render(request ,'layout.html')

def stores(request):
    return render(request, 'stores.html')


def haversine(lat1, lon1, lat2, lon2):
    R = 6371  # Earth's radius in km
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = (math.sin(dlat / 2) ** 2 +
         math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * 
         math.sin(dlon / 2) ** 2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return round(R * c, 2)  # Round to 2 decimal places


def grocery_stores_view(request):
    lat = request.GET.get('lat')
    lon = request.GET.get('lon')

    if not lat or not lon:
        return JsonResponse({"error": "Latitude and Longitude are required"}, status=400)

    try:
        lat = float(lat)
        lon = float(lon)
    except ValueError:
        return JsonResponse({"error": "Invalid coordinates"}, status=400)

    stores = get_nearby_grocery_stores(lat, lon)

    if not stores:
        return JsonResponse({"message": "No stores found within the specified radius"}, status=200)

    return JsonResponse(stores, safe=False)


def get_nearby_grocery_stores(lat, lon, radius=3000, max_retries=3, timeout=10):
    overpass_url = "https://overpass-api.de/api/interpreter"
    
    query = f"""
    [out:json][timeout:25];
    (
      node["shop"="supermarket"](around:{radius},{lat},{lon});
      node["shop"="convenience"](around:{radius},{lat},{lon});
      node["shop"="greengrocer"](around:{radius},{lat},{lon});
      node["shop"="deli"](around:{radius},{lat},{lon});
      node["shop"="grocery"](around:{radius},{lat},{lon});
    );
    out body;
    """
    
    headers = {
        'User-Agent': 'Django-App/1.0',
        'Accept': 'application/json'
    }
    
    for attempt in range(max_retries):
        try:
            response = requests.get(overpass_url, params={"data": query}, headers=headers, timeout=timeout)
            response.raise_for_status()
            data = response.json()
            break
        except (requests.exceptions.RequestException, ValueError) as e:
            print(f"Attempt {attempt+1} failed: {str(e)}")
            time.sleep(2 ** attempt)  # Exponential backoff
    else:
        return JsonResponse({"error": "Failed to fetch store data from Overpass API"}, status=500)

    stores = []
    for element in data.get("elements", []):
        tags = element.get("tags", {})

        if "name" not in tags:
            continue

        lat_val = element.get("lat")
        lon_val = element.get("lon")
        
        distance = haversine(lat, lon, lat_val, lon_val)
        
        stores.append({
            "name": tags["name"],
            "distance_km": distance,
            "google_maps_url": f"https://www.google.com/maps?q={lat_val},{lon_val}"
        })

    # Sort stores by distance
    stores.sort(key=lambda x: x["distance_km"])
    
    return stores
