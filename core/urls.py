from django.urls import path
from .views import page, submit

urlpatterns = [
    path('', page('index.html'), name='home'),
    path('about/', page('about.html'), name='about'),
    path('sermons/', page('sermons.html'), name='sermons'),
    path('ministries/', page('ministries.html'), name='ministries'),
    path('events/', page('events.html'), name='events'),
    path('gallery/', page('gallery.html'), name='gallery'),
    path('contact/', page('contact.html'), name='contact'),
    path('api/<str:kind>/', submit, name='submit'),
]
