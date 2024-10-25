from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import RegisterView, LogoutView, SubscriptionViewSet
from rest_framework.routers import DefaultRouter
from django.contrib.auth import views as auth_views
from django.http import HttpResponse

# Homepage view function
def homepage(request):
    return HttpResponse("Welcome to the Subscription Management System!")

# Set up the router for subscription endpoints
router = DefaultRouter()
router.register(r'subscriptions', SubscriptionViewSet, basename='subscription')

# URL patterns
urlpatterns = [
    path('', homepage, name='homepage'),  # Root URL shows the homepage
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('password_reset_done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
]

urlpatterns += router.urls
