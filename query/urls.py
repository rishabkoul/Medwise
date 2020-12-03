from django.urls import path
from query.views import create_query_view, docs_not_allowed_view, detail_query_view, edit_query_view, Delete_query

app_name = 'query'

urlpatterns = [
    path('create/', create_query_view, name='create'),
    path('delete/', Delete_query.as_view(), name='delete'),
    path('<slug>/', detail_query_view, name='detail'),
    path('<slug>/edit', edit_query_view, name='edit'),
    path('docs_not_allowed/', docs_not_allowed_view, name='docs_not_allowed'),
]
