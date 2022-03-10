from flask import Flask, request, render_template, jsonify
import requests
from flask_cors import CORS
from auth import check_token

app = Flask(__name__)
# Enable cors for frontend app
CORS(app)


@app.route("/protected", methods=["GET"])
def index():
    token_response = check_token(request)
    if token_response.get("error") != None:
        return token_response, token_response.get("code")
    return {"status": "Ok"}

@app.route("/admin", methods=["GET"])
def admin():
    headers = request.headers
    token = headers.get("api-key")
    if not token:
        return {"error": "Unauthorized"}, 401
    if token not in [item.get("token") for item in token_list]:
        return {"error": "Unauthorized"}, 401
    has_access = False
    for item in token_list:
        access_level = item.get("admin")
        if token == item.get("token"):
            has_access = access_level
            break
    if has_access is False:
        return {"error": "Not authorized"}, 403
            
    return {"status": "Ok"}

#Testing route
@app.route("/", methods=["GET"])
def home():
    return 'Hello World!'

# receives 2 parameters name and date and returns a json with link and error
# (request example: http://127.0.0.1:5000/movie?name=batman&date=2022-03-04)
@app.route("/movie", methods=["GET"]) 
def movie():

    try:
        # Auth
        token_response = check_token(request)
        if token_response.get("error") != None:
            return token_response, token_response.get("code")
        # dict with query parameters
        args = request.args
        name = args.get('name')
        date = args.get('date')

        # checks if name or date exists
        if not name or not date:
            return dict(link = None, error = "name or date is missing"), 400

        # url for data source
        url = f"https://www.cinemacity.ro/ro/data-api-service/v1/quickbook/10107/film-events/in-cinema/1807/at-date/{date}?attr=&lang=ro_RO"

        # make a request to url and store the movies list
        r = requests.get(url)
        response = r.json()
        films_ = response.get("body").get("films")

        # loops through the list and checks if the provided name is in the API response
        # if yes, returns a json with link and error (None), if no returns a json with link(None) and error
        for film in films_:
            if name.lower() in film["name"].lower():
                return dict(link = film["link"], error=None)
            
        return dict(link = None, error = "Not found"), 404

    except:
        return dict(link = None, error = "Not found"), 404


# receives 2 parameters name and date 
# returns a json with data list which contains a cinema name and events 
# events is a list with dictionaires containing auditoriums and event_time
@app.route("/search", methods=["GET"])
def search():
    
    try:
        # Auth
        token_response = check_token(request)
        if token_response.get("error") != None:
            return token_response, token_response.get("code")
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

# Only executed when calling the script directly
if __name__ == "__main__":
    app.run(debug=True)
