from django.urls import path
from api.views import SendEmailRegistrationView

urlpatterns = [
    path('register/', SendEmailRegistrationView.as_view(), name='user-registration'),
    
]
