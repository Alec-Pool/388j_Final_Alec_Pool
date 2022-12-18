from flask import Blueprint, render_template, url_for, redirect, request, flash
from flask_login import (
    LoginManager,
    current_user,
    login_required,
)

from ..forms import NameSearchForm, AttributeSearchForm, RestaurantReviewForm
from ..models import User, Review, Restaurant
from ..utils import current_time, process_query






main = Blueprint("main", __name__)



@main.route("/", methods=["GET", "POST"])
def index():

    return render_template("index.html")



@main.route("/restaurants/search", methods=["GET", "POST"])
@login_required
def search():
    nameForm = NameSearchForm()
    attributeForm = AttributeSearchForm()

    if nameForm.validate_on_submit():
        return redirect(url_for("main.query_results", query=nameForm.search_query.data+ " " + nameForm.location.data))
    
    if attributeForm.validate_on_submit():
        info = {
            'romance': attributeForm.romance.data,
            'occasion': attributeForm.occasion.data,
            'price': attributeForm.price.data,
        }
        #print(type(info), info)
        return redirect(url_for("main.query_results", query=info))

    return render_template("search.html", nameForm=nameForm, attributeForm=attributeForm)




@main.route("/restaurants/search-results/<query>", methods=["GET"])
def query_results(query):
    allRestaurants = Restaurant.objects()
    try:
        restaurants = process_query(query, allRestaurants)
    except ValueError as e:
        flash(str(e))
        return redirect(url_for("main.index"))

    restaurantObjs = {}

    for restaurant in restaurants:
        restaurantObjs[restaurant] = (Restaurant.objects(restaurant_details=restaurant).first())

    return render_template("query.html", restaurantObjs=restaurantObjs, orderedRestaurants=restaurants)




@main.route("/restaurants/reviews/<restaurant>", methods=["GET", "POST"])
def restaurant_reviews(restaurant):
    

    form = RestaurantReviewForm()
    

    if form.validate_on_submit() and current_user.is_authenticated:
        review = Review(
            commenter=current_user._get_current_object(),
            content=form.text.data,
            date=current_time(),
            restaurant_details=restaurant,
            romance=form.romance.data,
            price = "$" * form.price.data,
            recommend = form.recommend.data,
            occasion = form.occasion.data,
        )
        review.save()

        if Restaurant.objects(restaurant_details=restaurant).count() == 0:
            newRestaurant = Restaurant(
                restaurant_details = restaurant,
                reviews_list = [review],
                averageRomance = form.romance.data,
                averagePrice = "$" * form.price.data,
                averageRecommend = form.recommend.data,
                averageOccasion = form.occasion.data,
            )
            newRestaurant.save()

        elif Restaurant.objects(restaurant_details=restaurant).count() == 1:
            currRestaurant = Restaurant.objects(restaurant_details=restaurant)
            currRestaurant.update_one(push__reviews_list=review)
            currRestaurant = Restaurant.objects(restaurant_details=restaurant).first()
            currRestaurant.updateAverages()
            currRestaurant.save()

        else:
            print("ERROR")


        return redirect(request.path)

    reviews = Review.objects(restaurant_details=restaurant)

    restaurantObj = Restaurant.objects(restaurant_details=restaurant).first()

    #print(Restaurant.objects(restaurant_details=restaurant).count(), restaurantObj.averageRecommend)
    #print(restaurantObj.restaurant_details)


    return render_template(
        "restaurant_details.html", form=form, restaurant=restaurantObj, reviews=reviews, restaurantDetatils=restaurant
    )


@main.route("/user/<username>")
def user_detail(username):
    user = User.objects(username=username).first()
    reviews = Review.objects(commenter=user)

    return render_template("user_detail.html", username=username, reviews=reviews)



