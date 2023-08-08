from core.models import Product, ProductHistory, Profile, Store, UpdateNote
from django.contrib import admin
from django.utils.html import format_html

class ProductAdmin(admin.ModelAdmin):
    list_display = ('foto', 'name', 'price', 'min_price', 'followers')

    def foto(self, obj):
        return format_html(u'<img width="40px" src="{}" />', obj.url_image)

    def min_price(self, obj):
        return obj.min_price()

    def followers(self, obj):
        return len(obj.users.all())

# Register your models here.
admin.site.register(Product, ProductAdmin)
admin.site.register(ProductHistory)
admin.site.register(Profile)
admin.site.register(Store)
admin.site.register(UpdateNote)
