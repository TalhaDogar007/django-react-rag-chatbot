from django.urls import path
from .views import PDFUploadView, SearchView

urlpatterns = [
    path('upload/', PDFUploadView.as_view(), name='pdf-upload'),
    path('search/', SearchView.as_view(), name='search'),
]