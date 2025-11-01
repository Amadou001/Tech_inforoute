"""
URL configuration for Api_rest project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from graphene_django.views import GraphQLView
from django.views.decorators.csrf import csrf_exempt
from api.schema import schema 
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions

schema_view = get_schema_view(
    openapi.Info(
        title="INF37407 API",
        default_version='v1',
        description="API documentation for harvesting and dataset endpoints",
        terms_of_service="https://www.uqar.ca/",
        contact=openapi.Contact(email="bamadou634@gmail.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,  # if you want it open, set to False for auth-protected
    permission_classes=(permissions.AllowAny,),
)


urlpatterns = [
    path('', include('users.urls')),
    path('admin/', admin.site.urls),
    path('api/users/', include('users.urls')),
    path('api/', include('api.urls')),
    path("graphql/", csrf_exempt(GraphQLView.as_view(graphiql=True, schema=schema))),  # Interactive GraphQL IDE
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
]
