from django.contrib import admin
from websearch.models import Category, Page, UserProfile
#OR from .models import Category, Page



class PageAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'url')
    
admin.site.register(Category)
admin.site.register(Page, PageAdmin)
admin.site.register(UserProfile)
