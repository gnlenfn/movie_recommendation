from flask import Blueprint, render_template
from flask import Blueprint
from app.models import Review
from app.services import scraping_reviews


bp = Blueprint('main', __name__, url_prefix="/")

@bp.route("/hello/")
def hello():
    return "Hello, Test Message!"

@bp.route("/")
def index():
    rev = Review()
    table = scraping_reviews.get_current_movie_code(20)
    movie_list = table.sort_values(by='reserved', ascending=False)['title']

    return render_template("home_reserved.html", movie_list=movie_list, rev=rev)

@bp.route("/sorted/")
def sorted_by_date():
    rev = Review()
    table = scraping_reviews.get_current_movie_code(20)
    movie_list = table.sort_values(by='opening_date', ascending=False)['title']

    return render_template("home_open.html", movie_list=movie_list, rev=rev)