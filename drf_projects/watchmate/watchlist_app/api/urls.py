from django.urls import path,include
#from watchlist_app.api.views import movie_list,movie_details
from watchlist_app.api.views import (WatchListAV,WatchDetailAV,StreamPlatformAV,StreamPlatformDetailAV,ReviewList,ReviewDetail,ReviewCreate,StreamPlatformVS,UserReview)
from rest_framework.routers import DefaultRouter


router = DefaultRouter()
router.register('stream',StreamPlatformVS,basename='streamplatform')


urlpatterns = [
    path('list/',WatchListAV.as_view(),name = 'watchlist-list'),
    path('<int:pk>/',WatchDetailAV.as_view(),name='watchlist-detail'),
    path('<int:pk>/review-create/',ReviewCreate.as_view(),name = 'review-create'),#for creating spicific review
    path('<int:pk>/reviews/',ReviewList.as_view(),name = 'review-list'),#view all review of specific item
    path('review/<int:pk>/',ReviewDetail.as_view(),name = 'review-detail'),#open spicific review
    path('',include(router.urls)),
    # path('stream/',StreamPlatformAV.as_view(),name='stream'), 
    # path('stream/<int:pk>',StreamPlatformDetailAV.as_view(),name='streamplatform-detail'),
    # path('review/',ReviewList.as_view(),name='review-list'),
    # path('review/<int:pk>',ReviewDetail.as_view(),name='review-detail'),
    path('reviews/',UserReview.as_view(),name = 'user- review-detail')
]


# explantion two types of reviews
# Main Difference (Very Simple)
# URL	pk kis ka hai?	Kaam
# /stream/review/5/	 Review ka	Ek specific review (Jab tumhe direct review fetch/update/delete karna ho)
# /stream/2/review/	Stream ka	Us stream ke sab reviews(Us stream ke saare reviews ya uske related operations)

# or
# Case 1:
# /review/10/

# 👉 Review id 10

# Case 2:
# /stream/3/review/

# 👉 Stream id 3 ke all reviews