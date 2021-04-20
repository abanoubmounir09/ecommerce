from django.contrib import admin
from django.urls import path , include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework import routers
from rest_framework.urlpatterns import format_suffix_patterns
from . import views


#router = routers.DefaultRouter()
#router.register(r'pr', views.snippet_list)


urlpatterns = [
    #path('',include(router.urls)),
    path('snippets/', views.snippet_list,name="snippet_list"),
    path('categories/', views.category_list,name="category_list"),
    path('query/<str:cat>/<str:name>/', views.query_list,name="query_list"),
    path('prdid/<int:id>/', views.productbyid,name="productbyid"),
    path('test/', views.query_test,name="query_test"),
    path('home/',views.home,name="home"),
    path('rate/<str:id>/',views.rate_product,name="ratingItem"), 
    path('add/',views.addp,name="add"),
    path('order/',views.addtocard,name="order"),
    path('rate/<int:id>/',views.ratingItem,name="ratingItem"), 
    path('ownerproduct/',views.owenerProduct,name='ownerproduct')
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
   

#get error with path include
#urlpatterns = format_suffix_patterns(urlpatterns)