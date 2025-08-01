from django.urls import path
from . import views

urlpatterns = [
    # Publisher and Home URLs
    path("", views.home, name="home"),
    path('create-publisher/', views.create_publisher, name='create_publisher'),
    path('publisher-list/', views.publisher_list, name='publisher_list'),
    path('publisher-details/<int:publisher_id>/', views.publisher_detail, name='publisher_detail'),

    # Article URLs
    path('articles/create/', views.article_create, name='article_create'),
    path('articles/<int:pk>/update/', views.article_update, name='article_update'),
    path('articles/<int:pk>/delete/', views.article_delete, name='article_delete'),
    path('articles/', views.article_list, name='article_list'),
    path('articles/<int:pk>/', views.article_detail, name='article_detail'),
    
    # Approval URLs
    path('articles/<int:pk>/approve/', views.article_approve, name='article_approve'),
    path('newsletters/<int:pk>/approve/', views.newsletter_approve, name='newsletter_approve'),

    # Newsletter URLs
    path('newsletters/create/', views.newsletter_create, name='newsletter_create'),
    path('newsletters/<int:pk>/update/', views.newsletter_update, name='newsletter_update'),
    path('newsletters/<int:pk>/delete/', views.newsletter_delete, name='newsletter_delete'),
    path('newsletters/', views.newsletter_list, name='newsletter_list'),
    path('newsletters/<int:pk>/', views.newsletter_detail, name='newsletter_detail'),

    # Dashboard URLs
    path('journalist-dashboard/', views.journalist_dashboard_view, name='journalist_dashboard'),
    path('editor-dashboard/', views.editor_dashboard_view, name='editor_dashboard'),
    path('admin-dashboard/', views.admin_dashboard_view, name='admin_dashboard'),
    
     # Subscription URLs
    path('publisher/<int:publisher_id>/subscribe/', views.subscribe_publisher, name='subscribe_publisher'),
    path('journalist/<int:user_id>/', views.journalist_detail, name='journalist_detail'),
    path('journalist/<int:user_id>/subscribe/', views.subscribe_journalist, name='subscribe_journalist'),
]