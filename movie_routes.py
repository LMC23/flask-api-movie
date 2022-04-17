from flask import Blueprint, request
import requests
import logging

from middlewares import token_required

movie_blueprint = Blueprint("movie_blueprint", __name__)

logging.basicConfig(filename="app.log", filemode="a", format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# receives 2 parameters name and date and returns a json with link and error
# (request example: http://127.0.0.1:5000/movie?name=batman&date=2022-03-04)


@movie_blueprint.route("/movie", methods=["GET"])
@token_required
def movie():

    try:
        # dict with query parameters
        args = request.args
        name = args.get("name")
        date = args.get("date")

        # checks if name or date exists
        if not name or not date:
            return dict(link=None, error="name or date is missing"), 400

        # url for data source
        url = f"https://www.cinemacity.ro/ro/data-api-service/v1/quickbook/10107/film-events/in-cinema/1807/at-date/{date}?attr=&lang=ro_RO"  # noqa: E501

        # make a request to url and store the movies list
        r = requests.get(url)
        response = r.json()
        films_ = response.get("body").get("films")

        # loops through the list
        # checks if the provided name is in the API response
        # if yes, returns a json with link and error (None),
        # if no returns a json with link(None) and error
        for film in films_:
            if name.lower() in film["name"].lower():
                return dict(link=film["link"], error=None)
        return dict(link=None, error="Not found"), 404

    except Exception as e:
        error = str(e)
        logger.error(f"An error has occurred: {error}")
        return dict(link=None, error=error), 404
