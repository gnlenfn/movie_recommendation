from app import mongo
import uuid
from app.services import scraping_reviews
from models.baseline.predict import predict_neg_pos
from apscheduler.schedulers.background import BackgroundScheduler

class Review:
    def add_movie_review(self, title, num=100):
        code = scraping_reviews.get_movie_code(title)
        texts = scraping_reviews.scrap_reviews_of_num(code, num)
        poster = scraping_reviews.get_poster(code)
        prediction = []
        for idx, rev in enumerate(texts):
            print("predintion", idx)
            prediction.append(predict_neg_pos(rev))

        if sum(prediction) > 60:
            result = "yes"
        elif sum(prediction) < 40:
            result = "no"
        else:
            result = "soso"

        reviews = {
            "_id": uuid.uuid4().hex,
            "title": title,
            "code": code,
            'reviews': texts,
            'prediction': prediction,
            "recommend": result,
            "poster": poster
        }

        if mongo.db.review.find_one({"title": reviews['title']}):
            return {"error": "Movie is already in database"}, 400
        
        if mongo.db.review.insert_one(reviews):
            return reviews, 200
        
        return {"error": "Failed to add movie info"}, 400

    def get_data_from_db(self, title):
        code = scraping_reviews.get_movie_code(title)
        target = mongo.db.review.find_one({"code": code})
        return target

    def delete_review(self, title):
        mongo.db.review.remove({"title": title})
        return



review_database = Review()
sched = BackgroundScheduler(daemon=True)

def reset():
    df = scraping_reviews.get_current_movie_code(20)
    for i, t in enumerate(df['title']):
        print('title', i)
        review_database.add_movie_review(t, 100)

sched.add_job(reset, 'cron', hour='4')

# movie_list = mongo.db.review.distinct('title')
# for m in movie_list:
#     pred = review_database.get_data_from_db(m)['prediction']
#     if sum(pred) > 60:
#         result = "yes"
#     elif sum(pred) < 40:
#         result = "no"
#     else:
#         result = "soso"
#     print(result)
#     mongo.db.review.update_one({"title": m}, {"$set": {'recommend': result}})

if __name__ == '__main__':
    df = scraping_reviews.get_current_movie_code(20)
    review_database = Review()
    for i, t in enumerate(df['title']):
        print('title', i)
        print(review_database.add_movie_review(t, 100))
