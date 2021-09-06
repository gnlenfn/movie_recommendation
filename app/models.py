from app import mongo
import uuid
from app.services import scraping_reviews
from models.baseline.predict import predict_neg_pos
from apscheduler.schedulers.background import BackgroundScheduler

class Review:
    def add_movie_review(self, title, num=100):
        if mongo.db.review.find_one({"title": title}):
            return {"error": "Movie is already in database"}, 400

        code = scraping_reviews.get_movie_code(title)
        texts = scraping_reviews.scrap_reviews_of_num(code, num)
        poster = scraping_reviews.get_poster(code)
        date = scraping_reviews.get_opening_date(code)
        prediction = []
        for idx, rev in enumerate(texts):
            print("predintion", idx)
            prediction.append(predict_neg_pos(rev))

        if sum(prediction) / len(prediction) > 0.6:
            result = "yes"
        elif sum(prediction) / len(prediction) < 0.4:
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
            "poster": poster,
            "opening_date": date
        }
        
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
    for idx, title in enumerate(df['title']):
        print('title', idx)
        if mongo.db.review.find_one({"title": title}):
            mongo.db.review.update_one({'title': title}, {"$set" : {"reserved": df['ticketing']}})
        else:
            review_database.add_movie_review(title, 100)

sched.add_job(reset, 'cron', hour='11', minute='20')


if __name__ == '__main__':
    df = scraping_reviews.get_current_movie_code(20)
    for idx, title in enumerate(df['title']):
        print('title', idx)
        if mongo.db.review.find_one({"title": title}):
            mongo.db.review.update_one({'title': title}, {"$set" : {"reserved": df['reserved'][idx]}})
        else:
            review_database.add_movie_review(title, 100)
