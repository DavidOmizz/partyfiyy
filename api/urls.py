from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

app_name = 'api'
router = DefaultRouter()
# router.register(r'features', views.FeatureViewSet, basename='feature')
# router.register(r'pricing', views.PricingPlanViewSet, basename='pricing')
# router.register(r'blog', views.BlogPostViewSet, basename='blog')
# router.register(r'faqs', views.FAQViewSet, basename='faq')
# router.register(r'testimonials', views.TestimonialViewSet, basename='testimonial')

urlpatterns = [
    path('', include(router.urls)),
    path('faq', views.FAQViewSet.as_view({'get': 'list'}), name='faqs'),
    path('features', views.FeatureViewSet.as_view({'get': 'list'}), name='features'),
    path('testimonials', views.TestimonialViewSet.as_view({'get': 'list'}), name='testimonials-api'),
    path('contact/', views.ContactMessageAPIView.as_view(), name='api-contact'),
    path('privacy/', views.PrivacyPolicyViewSet.as_view({'get': 'list'}), name='api-privacy'),
    path('blog/', views.BlogPostViewSet.as_view({'get': 'list'}), name='api-blog-list'),
    path('blog/<slug:slug>/', views.BlogPostViewSet.as_view({'get': 'retrieve'}), name='api-blog-detail'),
]