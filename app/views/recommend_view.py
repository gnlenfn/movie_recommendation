from flask import Blueprint, render_template, request
from app.models import Review
from app import mongo
from app.forms import AddMovieForm

bp = Blueprint('query', __name__, url_prefix="/")

@bp.route('/recommend/', methods=['GET', 'POST'])
def recommend():
    rev = Review()
    form = AddMovieForm()
 
    if request.method == 'POST' and form.validate_on_submit():
        if mongo.db.review.find_one({'title': form.title.data}):
            target = rev.get_data_from_db(form.title.data)['recommend']
        else:
            rev.add_movie_review(form.title.data)
            target = rev.get_data_from_db(form.title.data)['recommend']

        print(target)

    elif request.method == 'GET':
        target = None
    
    return render_template('recommend.html', form=form, target=target, rev=rev)


