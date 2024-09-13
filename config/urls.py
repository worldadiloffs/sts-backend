from django.contrib import admin
from django.conf import settings
from django.urls import path, include, re_path
from django.views.static import serve
from django.conf.urls.i18n import i18n_patterns
from django.conf.urls.static import static
# from rest_framework_simplejwt.views import (
#     TokenRefreshView,
#     TokenVerifyView
# )
from drf_spectacular.views import (
    SpectacularAPIView, 
    SpectacularRedocView, 
    SpectacularSwaggerView
)
from config.settings import SPECTACULAR_SETTINGS

urlpatterns = [

    # global url
    re_path(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
    re_path(r'^static/(?P<path>.*)$', serve, {'document_root': settings.STATIC_ROOT}),
    path('admin/', admin.site.urls),
    path('api/v1/schema/', SpectacularAPIView.as_view(), name='schema'),
    # api documentation authentication 
    path('', include('account.urls', namespace='account')),
    path('', include('category.urls', namespace='category')),
    path('', include('product.urls', namespace='product')),
    path('', include('home.urls', namespace='home')),
    path('', include('blog.urls', namespace='blog')),
    path('', include('cashback.urls', namespace='cashback')),
    path('', include('ordersts.urls', namespace='ordersts')),
    path('', include('settings.urls', namespace='settings')),
    path('', include('calculator.urls', namespace='calculator')),
    # path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    # path('api/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    # path('api/v1/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    # path('', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
]



urlpatterns = [
    *i18n_patterns(*urlpatterns, prefix_default_language=False),
    ]

