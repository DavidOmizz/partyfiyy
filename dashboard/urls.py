from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path
from . import views

app_name = 'dashboard'
urlpatterns = [
    path('', views.dashboard_view, name='dashboard'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('testimonials/', views.testimonials_view, name='testimonials'),
    path('faqs/', views.faq_view, name='faq'),
    path('features/', views.features_view, name='features'),
    path('privacy/', views.privacy_view, name='privacy'),
    path('blog/', views.blog_view, name='blog'),
    # path('login/', LoginView.as_view(template_name='dashboard/login.html'), name='login'),
    # path('logout/', LogoutView.as_view(next_page='login/'), name='logout'),
]
