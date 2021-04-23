from django.contrib import admin
from .models import *


admin.empty_value_display = ''
admin.ModelAdmin.list_per_page = 100
#
class LinksInLine(admin.TabularInline):
    model = Links
    fields = ('url',)
    extra = 1
    can_delete = True

@admin.register(Musicitems)
class Musicitemsadmin(admin.ModelAdmin):
    list_display = ('name','is_active', 'your_price')
    fields = ('name', 'your_price','is_active','image' , 'description')
    search_fields = ['name','is_active', ]
    inlines = [
        LinksInLine,
    ]


class PricesInLine(admin.TabularInline):
    model = Prices
    fields = ('date','value','unit','un_seen_count')
    extra = 1
    can_delete = True

@admin.register(Links)
class Linksadmin(admin.ModelAdmin):
    autocomplete_fields  = ("musicitem",)
    list_display = ('musicitem','url',)
    fields =('musicitem','url',)
    search_fields = ['url','musicitem']
    inlines = [
        PricesInLine,
    ]

    # def get_model_perms(self, request):
    #     """
    #     Return empty perms dict thus hiding the model from admin index.
    #     """
    #     return {}
