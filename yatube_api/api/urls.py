from rest_framework_nested import routers
from rest_framework.authtoken import views

from django.urls import include, path

from .views import PostViewSet, GroupViewSet, CommentViewSet

router = routers.SimpleRouter()
# Вызываем метод .register с нужными параметрами
router.register(r'api/v1/posts', PostViewSet)
router.register(r'api/v1/groups', GroupViewSet)

posts_router = routers.NestedSimpleRouter(
    router, r'api/v1/posts', lookup='post')
posts_router.register(r'comments', CommentViewSet, basename='post-comments')


urlpatterns = [
    # Все зарегистрированные в router пути доступны в router.urls
    # Включим их в головной urls.py
    path('api/v1/api-token-auth/', views.obtain_auth_token),
    path(r'', include(router.urls)),
    path(r'', include(posts_router.urls)),
]
