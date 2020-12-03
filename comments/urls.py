from django.urls import path
from comments.views import create_comment_view, Delete_comment

app_name = 'comments'

urlpatterns = [
    path('create/<slug>', create_comment_view, name='create'),
    path('delete/<id>/', Delete_comment.as_view(), name='delete'),
]
