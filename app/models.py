from app import mongo
import uuid
from app.services import scraping_reviews
from models.baseline.predict import predict_neg_pos
from apscheduler.schedulers.background import BackgroundScheduler

class Review:
    def add_movie_review(self, title, num=100, current=False):
        if mongo.db.review.find_one({"title": title}):
            return {"error": "Movie is already in database"}, 400

        table = scraping_reviews.get_current_movie_code(20)
        if current:
            code = table[table['title'] == title]['code'].item()
            date = table[table['title'] == title]['opening_date'].item()
        
        else:
            code = scraping_reviews.get_movie_code(title)
            date = scraping_reviews.get_opening_date(code)
        
        texts = scraping_reviews.scrap_reviews_of_num(code, num)
        poster = scraping_reviews.get_poster(code)
        reserved = scraping_reviews.get_opening_date(code)
        if not texts:
            result = 'empty'
        else:
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
            "opening_date": date,
            "reserved" : reserved
        }
        
        if mongo.db.review.insert_one(reviews):
            return reviews, 200
        
        return {"error": "Failed to add movie info"}, 400

    def get_data_from_db(self, title):
        target = mongo.db.review.find_one({"title": title})
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


#if __name__ == '__main__':
df = scraping_reviews.get_current_movie_code(20)
for idx, title in enumerate(df['title']):
    print(title, idx)
    if mongo.db.review.find_one({"title": title}):
        mongo.db.review.update_one({'title': title}, {"$set" : {"reserved": df['reserved'][idx]}})
    else:
        review_database.add_movie_review(title, 100, current=True)
