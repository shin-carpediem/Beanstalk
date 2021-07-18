from rest_framework import routers
from .views import UserViewSet, NonLoginUserViewSet, CartUserViewSet, OrderViewSet, CategoryViewSet, AllergyViewSet, MenuViewSet, NomihoViewSet


router = routers.DefaultRouter()
router.register(r'user', UserViewSet)
router.register(r'non_login_user', NonLoginUserViewSet)
router.register(r'cart', CartUserViewSet)
router.register(r'order', OrderViewSet)
router.register(r'category', CategoryViewSet)
router.register(r'allergy', AllergyViewSet)
router.register(r'menu', MenuViewSet)
router.register(r'menu', NomihoViewSet)
