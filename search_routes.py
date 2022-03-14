from flask import Blueprint, request
import requests

from middlewares import token_required

search_blueprint = Blueprint('search_blueprint', __name__)

# receives 2 parameters name and date 
# returns a json with data list which contains a cinema name and events 
# events is a list with dictionaires containing auditoriums and event_time
@search_blueprint.route("/search", methods=["GET"])
@token_required
def search():
    
    try:

        # dict with query parameters
        args = request.args
        name = args.get('name')
        date = args.get('date')

        # checks if name or date exists
        if not name or not date:
            return dict(error = "name or date is missing"), 400

        # url for data source 
        url_search = "https://www.cinemacity.ro/ro/data-api-service/v1/quickbook/10107/films/until/2023-02-28?attr=&lang=ro_RO"

        # make a request to url and store the movies list
        r = requests.get(url_search)
        response = r.json()
        films_search = response.get("body").get("films")

        # loops through the list and checks if the provided name is in the API response
        for film in films_search:
            if name.lower() in film['name'].lower():

                # make a request to cinema city API for more information on the searched movie 
                film_id = film.get("id")
                url_theathre = f"https://www.cinemacity.ro/ro/data-api-service/v1/quickbook/10107/cinema-events/in-group/bucuresti/with-film/{film_id}/at-date/{date}?attr=&lang=ro_RO"
                r_theathre = requests.get(url_theathre)
                response_theathre = r_theathre.json()

                # stores data regarding cinemas and events
                cinemas = response_theathre.get("body").get("cinemas")
                events = response_theathre.get("body").get("events")
                cinema_info = []

                # loops through the cinemas 
                for cinema in cinemas:
                    cinema_name = cinema.get("displayName")
                    event_info = []

                    # add a dictionary to event_info list when the event corresponds with the current cinema and searched movie 
                    for event in events:
                        if event.get("cinemaId") == cinema.get("id") and event.get("filmId") == film_id:
                            event_Date_Time = event.get("eventDateTime")
                            auditorium_Tiny_Name = event.get("auditoriumTinyName")
                            d = dict(event_time = event_Date_Time, auditorium = auditorium_Tiny_Name)
                            event_info.append(d)

                    # create a new dict (d2) with cinema_name and event_info list and appends to cinema_info list
                    d2 = dict(cinema_name = cinema_name, events = event_info)
                    cinema_info.append(d2)

                # returns a json with all of the above
                return dict(data = cinema_info)

        return dict(eroor = "Not found"), 404

    except:
        return dict(error = "Not found"), 404