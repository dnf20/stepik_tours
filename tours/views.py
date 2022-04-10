from django.http import Http404, HttpResponseNotFound, HttpResponseServerError
from django.shortcuts import render


# Create your views here.


def main_view(request):
    departures = initialize_departures()
    tours = initialize_tours(departures)
    return render(request, "index.html", context={"departures": departures, "tours": tours})


def departure_view(request, departure: str):
    departures = initialize_departures()
    all_tours = initialize_tours(departures)
    context_departure = None
    tours = []
    for dept in departures:
        if dept["code"] == departure:
            context_departure = dept
            tours = all_tours[departure]
            break
    if context_departure is None:
        raise Http404
    return render(request, "departure.html",
                  context={"departures": departures, "departure": context_departure, "tours": tours})


def tour_view(request, id: int):
    departures = initialize_departures()
    tours_by_departures = initialize_tours(departures)
    context_tour = None
    for tours in tours_by_departures.values():
        for tour in tours:
            if tour["id"] == id:
                context_tour = tour
                break
        if context_tour is not None:
            break
    if context_tour is None:
        raise Http404
    return render(request, "tour.html", context={"departures": departures, "tour": context_tour})


def initialize_tours(departures):
    all_tours = {}
    i = 1
    for dept in departures:
        all_tours[dept["code"]] = [{"id": j, "hotel": f"hotel {j}", "departure": dept["name"]} for j in range(i, i + 6)]
        i = i + 6
    return all_tours


def initialize_departures():
    return [
        {"code": "msk", "name": "Из Москвы"},
        {"code": "spb", "name": "Из Петербурга"},
        {"code": "nsk", "name": "Из Новосибирска"},
        {"code": "ekb", "name": "Из Екатеринбурга"},
        {"code": "kzn", "name": "Из Казани"},
    ]


def custom_handler404(request, exception):
    return HttpResponseNotFound('Ресурс не найден!')


def custom_handler500(request):
    return HttpResponseServerError('Ошибка сервера!')
