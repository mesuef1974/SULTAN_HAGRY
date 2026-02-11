from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.plan_list, name='dashboard'),
    path('plan/', include([
        path('', views.plan_list, name='plan_list'),
    ])),
    path('auth/login/', views.login_view, name='login'),
    path('auth/logout/', views.logout_view, name='logout'),
]