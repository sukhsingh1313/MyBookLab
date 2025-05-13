from django.contrib import admin
from .models import BooksLibrary, social_links, topbar_changes, Categories,Contact

# Register your models here.
admin.site.register(Categories)

admin.site.register(social_links)
admin.site.register(topbar_changes)


class BooksLibraryAdmin(admin.ModelAdmin):
     list_display = ('title', 'author', 'slug')
     prepopulated_fields = {'slug': ('title',)}

admin.site.register(BooksLibrary, BooksLibraryAdmin)

class ContectAdmin(admin.ModelAdmin):
     list_display = ('name', 'message')

admin.site.register(Contact,ContectAdmin)