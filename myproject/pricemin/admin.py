from django.contrib import admin

# Register your models here.
#from django.contrib.auth.models import User
from pricemin.models import Town, Adress, Product, Events
from media.models import News

#class PriceminAdmin(admin.ModelAdmin):
 #   readonly_fields = ('id',)
#   list_display = ('id',)

admin.site.register(Town)
admin.site.register(Adress)
admin.site.register(Product)
admin.site.register(Events)
#admin.site.register(User, PriceminAdmin)

admin.site.register(News)

