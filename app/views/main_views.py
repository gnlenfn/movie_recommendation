from flask import Blueprint, render_template
from app.services import scraping_reviews
from flask import Blueprint
from app.models import Review


bp = Blueprint('main', __name__, url_prefix="/")

@bp.route("/hello/")
def hello():
    return "Hello, Test Message!"

@bp.route("/")
def index():
    rev = Review()
    movie_list = scraping_reviews.get_current_movie_code(20)['title']

    return render_template("home.html", movie_list=movie_list, rev=rev)

