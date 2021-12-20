from rest_framework.routers import SimpleRouter
from rest_framework.authtoken import views

from django.urls import include, path

from .views import PostViewSet, GroupViewSet, CommentViewSet

# Создаётся роутер
router = SimpleRouter()
# Вызываем метод .register с нужными параметрами
router.register('api/v1/posts', PostViewSet)

router.register(r'api/v1/posts/(?P<post_id>\d+)/comments/(?P<comment_id>\d+)',
                CommentViewSet, basename='Comment')

router.register('api/v1/groups', GroupViewSet)

urlpatterns = [
    # Все зарегистрированные в router пути доступны в router.urls
    # Включим их в головной urls.py
    path('api/v1/api-token-auth/', views.obtain_auth_token),
    path('', include(router.urls)),
]
