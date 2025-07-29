from django.urls import path
from . import views

app_name = 'djangoapp'
urlpatterns = [
    # Path untuk halaman utama
    path('', views.get_dealerships, name='index'),

    # Path untuk otentikasi
    path('register/', views.registration_request, name='register'),
    path('login/', views.login_request, name='login'),
    path('logout/', views.logout_request, name='logout'),

    # Path untuk halaman statis
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),

    # Path untuk dealer dan review
    path('dealer/<int:dealer_id>/', views.get_dealer_details, name='dealer_details'),
    path('dealer/<int:dealer_id>/add_review/', views.add_review, name='add_review'),

    # Path BARU untuk sentiment analyzer
    path('sentiment/', views.sentiment_analyzer, name='sentiment_analyzer'),
]