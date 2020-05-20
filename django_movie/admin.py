from ckeditor_uploader.widgets import CKEditorUploadingWidget
from django.contrib import admin

# Register your models here.
from django import forms
from django.utils.safestring import mark_safe

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


class MovieAdminForm(forms.ModelForm):
    description = forms.CharField(label='Описание', widget=CKEditorUploadingWidget())

    class Meta:
        model = Movie
        fields = '__all__'


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'url')
    list_display_links = ['name']


class ReviewInLine(admin.StackedInline):
    model = Review
    extra = 1
    readonly_fields = ['name', 'email']


class MovieShotsInLine(admin.TabularInline):
    model = MovieShots
    extra = 1
    readonly_fields = ['get_image']

    def get_image(self, obj):
        return mark_safe(f'<img src={obj.image.url} width="100" height="100">')

    get_image.short_description = 'Изображение'


@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'url', 'draft')
    list_filter = ['category', 'year']
    search_fields = ['title', 'category__name']
    inlines = [MovieShotsInLine, ReviewInLine]
    list_editable = ("draft",)
    actions = ['publish', 'unpublished']
    form = MovieAdminForm
    save_on_top = True
    save_as = True
    list_editable = ['draft']
    readonly_fields = ['get_poster']
    fieldsets = (
        (None, {
            "fields": ('description', ('poster', 'get_poster'))
        }),
    )

    def get_poster(self, obj):
        return mark_safe(f'<img src={obj.poster.url} width="350" height="550">')

    get_poster.short_description = 'Постер'

    def publish(self, request, queryset):
        row_update = queryset.update(draft=False)
        if row_update == 1:
            message_bit = '1 запись обновлена'
        else:
            message_bit = f'{row_update} записей были  обновлены'
        self.message_user(request, f'{message_bit}')

    publish.short_description = 'Опубликовать'
    publish.allowed_permissions = ('change',)

    def unpublished(self, request, queryset):
        row_update = queryset.update(draft=True)
        if row_update == 1:
            message_bit = '1 запись обновлена'
        else:
            message_bit = f'{row_update} записей были  обновлены'
        self.message_user(request, f'{message_bit}')

    unpublished.short_description = 'Снять с публикации'
    unpublished.allowed_permissions = ('change',)


@admin.register(Review)
class AdminReview(admin.ModelAdmin):
    list_display = ['name', 'email', 'parent', 'movie', 'id']
    readonly_fields = ['name', 'email']


@admin.register(Actors)
class AdminActors(admin.ModelAdmin):
    list_display = ['name', 'age', 'get_image']
    readonly_fields = ['get_image']

    def get_image(self, obj):
        return mark_safe(f'<img src={obj.image.url} width="50" height="50">')

    get_image.short_description = 'Изображение'


@admin.register(MovieShots)
class AdminMovieShots(admin.ModelAdmin):
    list_display = ['title', 'description', 'movie', 'get_image']

    def get_image(self, obj):
        return mark_safe(f'<img src={obj.image.url} width="50" height="50">')

    get_image.short_description = 'Изображение'
    readonly_fields = ['get_image']


admin.site.register(RatingStar)
admin.site.register(Rating)
admin.site.register(Genre)
admin.site.site_title = 'Django Movies'
admin.site.site_header = 'Django Movies'
