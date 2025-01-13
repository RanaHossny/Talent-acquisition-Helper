from django.urls import path
from .views import UploadPDFsView

urlpatterns = [
    path('upload-pdf/', UploadPDFsView.as_view(), name='upload_pdf'),
]
