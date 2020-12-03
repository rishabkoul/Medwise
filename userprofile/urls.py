from django.urls import path
from userprofile.views import create_profile_view, edit_profile_view, detail_profile_view

app_name = 'userprofile'

urlpatterns = [
    path('create/', create_profile_view, name='create'),
    path('profiles/<slug>/', detail_profile_view, name='detail'),
    path('edit/', edit_profile_view, name='edit'),
]
