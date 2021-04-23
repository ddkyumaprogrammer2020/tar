from django.conf.urls import url
from Scraping.tasks import get_prices
urlpatterns = [
    url(r'get-prices/', get_prices),
]

