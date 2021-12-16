from rest_framework.routers import SimpleRouter
from rest_framework.authtoken import views

from django.urls import include, path

from .views import PostViewSet, GroupViewSet, CommentiewSet

# Создаётся роутер
router = SimpleRouter()
# Вызываем метод .register с нужными параметрами
router.register('api/v1/posts', PostViewSet)
router.register('api/v1/groups', GroupViewSet)
router.register('api/v1/posts/<post_id>/comments/<comment_id>', CommentiewSet)


# В роутере можно зарегистрировать любое количество пар "URL, viewset":
# например
# router.register('owners', OwnerViewSet)
# Но нам это пока не нужно

urlpatterns = [
    # Все зарегистрированные в router пути доступны в router.urls
    # Включим их в головной urls.py
    path('api/v1/api-token-auth/', views.obtain_auth_token),
    path('', include(router.urls)),
]
