from rest_framework import viewsets
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token  # Импортируй Token из правильного модуля
from rest_framework.response import Response
from django.contrib.auth.models import User
from .models import Course, Purchase
from .models import UserProgress
from rest_framework import permissions
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.permissions import IsAuthenticated
from .serializers import ProfileSerializer, UserProgressSerializer, CourseSerializer, UserSerializer, PurchaseSerializer

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class CustomAuthToken(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                         context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)  # Используй Token.objects
        return Response({
            'token': token.key,
            'user_id': user.pk,
            'email': user.email
        })
    

class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Кастомный пермишен: разрешает редактирование только владельцу курса.
    """
    def has_object_permission(self, request, view, obj):
        # Разрешаем GET, HEAD, OPTIONS запросы всем.
        if request.method in permissions.SAFE_METHODS:
            return True

        # Разрешаем редактирование только владельцу курса.
        return obj.owner == request.user
    

class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

    def perform_create(self, serializer):
        # Автоматически назначаем текущего пользователя как владельца курса.
        serializer.save(owner=self.request.user)


class UserProgressViewSet(viewsets.ModelViewSet):
    queryset = UserProgress.objects.all()
    serializer_class = UserProgressSerializer

# 

class RegisterView(APIView):
    permission_classes = [AllowAny] 
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        serializer = ProfileSerializer(user)
        return Response(serializer.data)

class PurchaseView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, course_id):
        try:
            course = Course.objects.get(id=course_id)
        except Course.DoesNotExist:
            return Response({'error': 'Курс не найден'}, status=status.HTTP_404_NOT_FOUND)

        # Проверяем, не купил ли пользователь курс ранее
        if Purchase.objects.filter(user=request.user, course=course).exists():
            return Response({'error': 'Курс уже куплен'}, status=status.HTTP_400_BAD_REQUEST)

        purchase = Purchase.objects.create(user=request.user, course=course)
        serializer = PurchaseSerializer(purchase)
        return Response(serializer.data, status=status.HTTP_201_CREATED)