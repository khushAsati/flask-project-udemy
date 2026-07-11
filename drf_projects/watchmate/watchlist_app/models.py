from django.db import models
from django.core.validators import MinValueValidator,MaxValueValidator
from django.contrib.auth.models import User
# Create your models here.


class StreamPlatform(models.Model):
    name = models.CharField(max_length=30)
    about = models.CharField(max_length=50)
    website = models.URLField(max_length=100)
    
    def __str__(self):
        return self.name 


class WatchList(models.Model):#platform has been connected with thiese movies one streamplatform can have multiplemovies
    title = models.CharField(max_length=50)
    storyline = models.CharField(max_length=200)
    platform = models.ForeignKey(StreamPlatform, on_delete=models.CASCADE,related_name ="watchlist")
    active = models.BooleanField(default = True)
    created = models.DateTimeField(auto_now_add=True)
    avg_rating = models.FloatField(default=0)
    avg_number = models.IntegerField(default=0)
    #This is a One-to-Many relationship (one platform → many movies).
    #To connect these tables, we add a foreign key in WatchList that references StreamPlatform.




   
    def __str__(self):
        return self.title
    
class Review(models.Model):
    userreview = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    rating = models.PositiveIntegerField(validators=[MinValueValidator(1),MaxValueValidator(5)])
    description = models.CharField(max_length=200,null=True)
    watchlist= models.ForeignKey(WatchList,on_delete=models.CASCADE,related_name="reviews")
    active = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    update = models.DateTimeField(auto_now=True)
      
    def __str__(self):
        user_str = f"{self.userreview.username} - " if self.userreview else ""
        return user_str + str(self.rating) + " : " + self.watchlist.title

class UserReview(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    review = models.ForeignKey(Review, on_delete=models.CASCADE, related_name='user_reviews')
    rating = models.PositiveIntegerField(validators=[MinValueValidator(1),MaxValueValidator(5)])
    description = models.CharField(max_length=200, null=True)
    created = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ['user', 'review']  # One review per user per review
    
    def __str__(self):
        return f"{self.user.username} - {self.review.watchlist.title} - {self.rating}"

# Think of It Like This:
# Imagine you have two tables:

# StreamPlatform (which stores details about streaming services like Netflix, Prime Video, etc.)

# WatchList (which stores movies and TV shows available on those platforms)

# ((((Each movie in the WatchList must belong to one streaming platform. But one platform can have multiple movies.

# This is a One-to-Many relationship (one platform → many movies).)))))

# To connect these tables, we add a foreign key in WatchList that references StreamPlatform.
#