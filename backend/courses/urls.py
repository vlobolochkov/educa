from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserViewSet, CustomAuthToken, CourseViewSet, UserProgressViewSet, RegisterView, ProfileView, PurchaseView

router = DefaultRouter()
router.register(r'users', UserViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('api-token-auth/', CustomAuthToken.as_view()),
    path('register/', RegisterView.as_view(), name='register'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('courses/<int:course_id>/purchase/', PurchaseView.as_view(), name='purchase'),
    path('courses/', CourseViewSet.as_view({'get': 'list', 'post': 'create'}), name='course-list'),
]

router = DefaultRouter()
router.register(r'courses', CourseViewSet)  # Регистрируем маршруты для курсов
router.register(r'progress', UserProgressViewSet)  # Регистрируем маршруты для прогресса
