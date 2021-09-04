from flask import Blueprint, render_template
from app.models import Review
from models.baseline.predict import predict_neg_pos

# 리뷰보기 페이지 만들어야함 + html
bp = Blueprint('review', __name__, url_prefix="/reviews/")

@bp.route('/details/<string:title>/', methods=['GET'])
def show_details(title):
    rev = Review()
    pred = rev.get_data_from_db(title)['prediction']
    review = rev.get_data_from_db(title)['reviews']
    pos, neg = [], []
    for p, r in zip(pred, review):
        if p == 1 and len(pos) < 3 and r != "":
            pos.append(r)
        elif p == 0 and len(neg) < 3 and r != "" :
            neg.append(r)

        if len(pos) == len(neg) == 3:
            break
    
    return render_template('reviews.html', pos_list=pos, neg_list=neg, title=title)