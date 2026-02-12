from django.urls import path, include
from coredata.views import dashboard_views, plan_views, auth_views
from django.contrib.auth import views as auth_builtin_views

urlpatterns = [
    # Main Site
    path('', dashboard_views.dashboard_view, name='dashboard'),
    
    # Operational Plan
    path('plan/', include([
        path('', plan_views.plan_list, name='plan_list'),
        path('item/<int:pk>/execute/', plan_views.plan_edit_modal, name='execute_item'),
        path('item/<int:pk>/execute/save/', plan_views.plan_edit_save, name='execute_item_save'),
        path('item/<int:pk>/evaluate/', plan_views.plan_evaluate_modal, name='evaluate_item'),
        path('item/<int:pk>/evaluate/save/', plan_views.plan_evaluate_save, name='evaluate_item_save'),
        path('item/<int:pk>/evidence/', plan_views.plan_upload_evidence_modal, name='upload_evidence'),
        path('item/<int:pk>/evidence/save/', plan_views.plan_upload_evidence_save, name='upload_evidence_save'),
    ])),
    
    # Authentication
    path('auth/login/', auth_views.CustomLoginView.as_view(), name='login'),
    path('auth/logout/', auth_builtin_views.LogoutView.as_view(), name='logout'),
    
    # Reports
    path('admin/reports/activity/', dashboard_views.dashboard_view, name='activity_report'),
]