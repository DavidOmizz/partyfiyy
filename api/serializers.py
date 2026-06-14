from rest_framework import serializers
from dashboard.models import *


class FeatureSerializer(serializers.ModelSerializer):
    class Meta:
        model = Feature
        fields = ['id', 'title', 'image' ,'description', 'order']


# class PricingPlanSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = PricingPlan
#         fields = ['id', 'name', 'plan_type', 'price', 'currency', 'billing_period', 
#                   'features', 'description', 'is_popular', 'order']


# class BlogPostSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = BlogPost
#         fields = ['id', 'title', 'slug', 'excerpt', 'content', 'featured_image',
#                   'author', 'category', 'published_at', 'created_at']


class FAQSerializer(serializers.ModelSerializer):
    class Meta:
        model = FAQ
        fields = ['id', 'question', 'answer']


class TestimonialSerializer(serializers.ModelSerializer):
    class Meta:
        model = Testimonial
        fields = ['id', 'client_name', 'client_title', 'client_company', 'client_image',
                  'content', 'rating', 'order']


class ContactMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContactMessage
        fields = ['id', 'full_name', 'company_name', 'email', 'phone', 'subject', 'message', 'created_at']
        read_only_fields = ['id', 'created_at']


class SiteSettingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = SiteSettings
        fields = ['contact_email', 'contact_phone', 'contact_address',
                  'facebook_url', 'twitter_url', 'instagram_url', 'linkedin_url',
                  'site_title', 'site_description']


class PrivacyPolicySerializer(serializers.ModelSerializer):
    class Meta:
        model = PrivacyPolicy
        fields = ['id', 'title', 'content', 'effective_date', 'last_updated']


class BlogPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = BlogPost
        fields = ['id', 'title', 'slug', 'content', 'image',
                  'author', 'category', 'is_published', 'created_at']
