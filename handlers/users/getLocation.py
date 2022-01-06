from geopy.geocoders import Nominatim


async def defineLocation(latitude, longitude):
    geolocator = Nominatim(user_agent="geoapiExercises")
    coordinates = str(latitude)+","+str(longitude)
    location = geolocator.reverse(coordinates)
    try:
        return location.raw["address"]["locality"], location.raw["address"]["house_number"]
    except:
        return location.address.split(",")[1:2][0]

