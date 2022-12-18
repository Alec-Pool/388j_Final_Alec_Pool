from flask_login import UserMixin
from datetime import datetime
from . import db, login_manager
from . import config
from .utils import current_time
import base64

import statistics
from statistics import mode


@login_manager.user_loader
def load_user(user_id):
    return User.objects(username=user_id).first()


class User(db.Document, UserMixin):
    username = db.StringField(required=True, unique=True)
    email = db.EmailField(required=True, unique=True)
    password = db.StringField(required=True)

    # Returns unique string identifying our object
    def get_id(self):
        return self.username


class Review(db.Document):
    commenter = db.ReferenceField(User, required=True)
    content = db.StringField(required=True, min_length=5, max_length=500)
    date = db.StringField(required=True)
    restaurant_details = db.StringField(required=True, min_length=1, max_length=100)
    romance = db.StringField(required=True)
    price = db.StringField(required=True)
    recommend = db.IntField(required=True)
    occasion = db.StringField(required=True)



class Restaurant(db.Document):
    restaurant_details = db.StringField(required=True)

    reviews_list = db.ListField(required=True)

    averageRomance = db.StringField(required=True)
    averagePrice = db.StringField(required=True)
    averageRecommend = db.FloatField(required=True)
    averageOccasion = db.StringField(required=True)

    def updateAverages(self):
        numReviews = len(self.reviews_list)

        romanceList = []
        priceList = []
        occasionList = []

        totalRecommend = 0.0

        for review in self.reviews_list:
            romanceList.append(review.romance)
            priceList.append(review.price)
            occasionList.append(review.occasion)
            totalRecommend += review.recommend
        
        self.averageRomance = mode(romanceList)
        self.averageOccasion = mode(occasionList)
        self.averagePrice = mode(priceList)
        self.averageRecommend = round(totalRecommend / numReviews, 2)

