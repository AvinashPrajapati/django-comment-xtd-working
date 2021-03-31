from django.urls import path,include
from .views import home, userProfile,postDetail,newsletter_register,verify,delete_suscription

app_name='authentication'

urlpatterns = [
    path('', home, name='home'),
    path('post/<slug>/', postDetail, name='postDetail'),
    path('accounts/profile', userProfile, name='userProfile'),
    path('newsletter/', newsletter_register, name='newsletter_register'),
    path('verify/<token>/', verify, name='verify'),
    path('unsuscribe/<token>/', delete_suscription, name='delete_suscription'),
]
