from rest_framework import serializers
from .models import *

# User = get_user_model()
class PricesSerializer(serializers.ModelSerializer):

    class Meta:
        model = Prices
        fields = ('date','value','unit','un_seen_count')



class MusicitemsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Musicitems
        fields = ('name', 'your_price','is_active','_links','image','description')

class LinksSerializer(serializers.ModelSerializer):
    class Meta(MusicitemsSerializer.Meta):
        model = Links
        fields = ('url','musicitem')

