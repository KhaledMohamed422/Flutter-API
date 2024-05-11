from django.urls import path, include
from rest_framework import routers
from . import views
from .views import ProductViewSet, CardViewSet, FavoriteViewSet

router = routers.DefaultRouter()
router.register(r'products', ProductViewSet)
router.register(r'cards', CardViewSet)
router.register(r'favorites', FavoriteViewSet)

urlpatterns = [
    # Auth
    path('api/login/', views.login_view, name='api_login'),
    path('api/register/', views.register_view, name='api_register'),
    path('api/logout/', views.logout_view, name='api_logout'),

    # Profile
    path('api/profile/', views.get_profile, name='get_profile'),
    path('api/profile/update/', views.update_profile, name='update_profile'),


    path('api/user/<int:user_id>/cards/<int:card_id>/', views.user_card_detail, name='user_card_detail'),
    path('api/user/<int:user_id>/favorites/<int:favorite_id>/', views.user_favorite_detail, name='user_favorite_detail'),

    # Include router URLs
    path('api/', include(router.urls)),
    
    
]
