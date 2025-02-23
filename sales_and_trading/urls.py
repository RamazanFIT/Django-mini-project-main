from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path, re_path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions

schema_view = get_schema_view(
    openapi.Info(
        title="Sales and Trading API",
        default_version="v1",
        description="API documentation for Sales and Trading App",
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)

urlpatterns = [
    path("admin/", admin.site.urls),
    path(
        "admin-panel/",
        include("adminpanel.urls", namespace="adminpanel"),
    ),
    path(
        "",
        include("frontend.urls", namespace="frontend"),
    ),
    # Existing APIs
    path(
        "api/users/",
        include("users.urls"),
    ),
    path(
        "api/products/",
        include("products.urls"),
    ),
    path(
        "api/trading/",
        include("trading.urls"),
    ),
    path(
        "api/sales/",
        include("sales.urls"),
    ),
    path(
        "api/analytics/",
        include("analytics.urls"),
    ),
    # Swagger
    re_path(
        r"^swagger(?P<format>\.json|\.yaml)$",
        schema_view.without_ui(cache_timeout=0),
        name="schema-json",
    ),
    path(
        "swagger/",
        schema_view.with_ui("swagger", cache_timeout=0),
        name="schema-swagger-ui",
    ),
    path(
        "redoc/",
        schema_view.with_ui("redoc", cache_timeout=0),
        name="schema-redoc",
    ),
]

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT,
    )
