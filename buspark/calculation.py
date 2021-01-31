import requests


def get_coordinates(address):
    try:
        url = 'https://nominatim.openstreetmap.org/search/' + \
            address + '?format=json'
    except TypeError:
        return None
    response = requests.get(url).json()
    try:
        latitude = response[0]["lat"]
        longitude = response[0]["lon"]
    except IndexError:
        return None
    coordinates = [longitude, latitude]
    return coordinates


def get_distance(start, finish):
    start_coordinates = get_coordinates(start)
    finish_coordinates = get_coordinates(finish)
    if not start_coordinates or not finish_coordinates:
        return {'distance': None,
                'status_message': 'Точки маршрута заданы некорректно'}
    else:
        url = 'http://router.project-osrm.org/route/v1/driving/' + \
        ','.join(start_coordinates) + ';' + ','.join(finish_coordinates) + '?overview=false'
        response = requests.get(url).json()
        try:
            distance = response['routes'][0]['distance']
            status_message = 'Маршрут проложен'
        except KeyError:
            if response['code'] == "NoRoute":
                status_message = 'Не найдено маршрута между точками'
            else:
                status_message = 'Точки маршрута заданы некорректно'
            distance = None
        return {'distance': distance, 'status_message': status_message}