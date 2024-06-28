from django.contrib import admin
from cinema.models import *
# Register your models here.

class VideoProductAdmin(admin.ModelAdmin):
    list_display = ['title', 'release_year', 'moderated']
    actions = ['approve_selected', 'reject_selected']

    def approve_selected(self, request, queryset):
        queryset.update(moderated=True)

    def reject_selected(self, request, queryset):
        queryset.update(moderated=False)

    approve_selected.short_description = "Одобрить выбранные фильмы"
    reject_selected.short_description = "Отклонить выбранные фильмы"



admin.site.register(VideoProduct, VideoProductAdmin)
admin.site.register(Director)
admin.site.register(OriginalTitle)
admin.site.register(ProductType)
admin.site.register(Actor)
admin.site.register(Release_Year)
admin.site.register(Rating)
admin.site.register(RatingStar)
admin.site.register(Bookmark)