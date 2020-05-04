from django.contrib import admin

# Register your models here.
from .models import (
    RatingStar,
    Rating,
    Review,
    Actors,
    Category,
    MovieShots,
    Movie,
    Genre,
)

admin.site.register(RatingStar)
admin.site.register(Rating)
admin.site.register(Review)
admin.site.register(Actors)
admin.site.register(Category)
admin.site.register(MovieShots)
admin.site.register(Movie)
admin.site.register(Genre)
