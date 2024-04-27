import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URI')
db = SQLAlchemy(app)
CORS(app)

class Conference(db.Model):
    __tablename__ = 'conferences'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, nullable=False)
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date, nullable=False)
    location = db.Column(db.String(255), nullable=False)
    speakers = db.Column(db.JSON, nullable=False)
    website = db.Column(db.String(255), nullable=False)
    overall_rating = db.Column(db.Numeric(3,1), nullable=False)

class Review(db.Model):
    __tablename__ = 'reviews'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    conference_id = db.Column(db.Integer, db.ForeignKey('conference.id'))
    description = db.Column(db.Text, nullable=False)
    rating = db.Column(db.Numeric(3,1), nullable=False)

@app.route('/calculate-overall-rating')
def calculate_overall_rating():
    conferences = Conference.query.all()
    for conference in conferences:
        reviews = Review.query.filter_by(conference_id=conference.id).all()
        if reviews:
            ratings = [review.rating for review in reviews]
            average_rating = sum(ratings) / len(ratings)
            print(f"Overall rating for conference {conference.id}: {average_rating}")
        else:
            print(f"No reviews found for conference {conference.id}")

if __name__ == "__main__":
    calculate_overall_rating()
