from django.urls import path
from .views import SignUpView, LoginView,UserCollectionRetrieveView

urlpatterns = [
    path('auth/signup/', SignUpView.as_view(), name='signup'),
    path('auth/login/', LoginView.as_view(), name='login'),
    path('collection/', UserCollectionRetrieveView.as_view(), name='user-collection-retrieve'),

]
