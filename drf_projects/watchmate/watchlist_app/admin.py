from django.contrib import admin
from watchlist_app.models import WatchList,StreamPlatform,Review,UserReview


# Inline for UserReview to show inside Review
class UserReviewInline(admin.TabularInline):
    model = UserReview
    extra = 1  # Number of empty forms to show
    fields = ['user', 'rating', 'description']
    


# Customize Review admin to include UserReview
@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ['rating', 'watchlist', 'active', 'created']
    list_filter = ['rating', 'active', 'created']
    search_fields = ['watchlist__title', 'description']
    inlines = [UserReviewInline]


# Register your models here.
admin.site.register(WatchList)
admin.site.register(StreamPlatform)
# Don't register UserReview separately - it's now inline in Review