"""tar URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from tar import settings
from Scraping.views import HomePageView
from Scraping import views
admin.autodiscover()

admin.site.site_header = "Musical_Instruments Admin"
admin.site.site_title = "Musical_Instruments Admin Portal"
admin.site.index_title = "Welcome to Musical_Instruments Portal"


urlpatterns = [
    path('admin/', admin.site.urls),
    path(r'scraping/', include('Scraping.urls')),
    path('', HomePageView.as_view(), name='home'),
    path('musicitems/', views.MusicitemsList.as_view()),
    path('musicitems/<int:pk>/', views.MusicitemsDetail.as_view()),
    path('links/', views.LinksList.as_view()),
    path('links/<int:pk>/', views.MusicitemsDetail.as_view()),
    path('prices/', views.PricesList.as_view()),
    path('prices/<int:pk>/', views.PricesDetail.as_view()),
]




if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        path(r'^__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns
