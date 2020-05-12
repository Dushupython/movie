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


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'url')
    list_display_links = ['name']


class ReviewInLine(admin.StackedInline):
    model = Review
    extra = 1
    readonly_fields = ['name', 'email']

@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'url', 'draft')
    list_filter = ['category', 'year']
    search_fields = ['title', 'category__name']
    inlines = [ReviewInLine]
    save_on_top = True
    save_as = True
    list_editable = ['draft']

@admin.register(Review)
class AdminReview(admin.ModelAdmin):
    list_display = ['name', 'email', 'parent', 'movie', 'id']
    readonly_fields = ['name', 'email']


admin.site.register(RatingStar)
admin.site.register(Rating)
admin.site.register(Actors)
admin.site.register(MovieShots)
admin.site.register(Genre)
