from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.core.mail import send_mail
from django.conf import settings
from dashboard.models import *
from rest_framework.views import APIView

from .serializers import *



# Create your views here.

class FeatureViewSet(viewsets.ReadOnlyModelViewSet):
    """API endpoint for retrieving features."""
    queryset = Feature.objects.all()
    serializer_class = FeatureSerializer
    ordering = ['order', 'created_at']

class TestimonialViewSet(viewsets.ReadOnlyModelViewSet):
    """API endpoint for retrieving testimonials."""
    queryset = Testimonial.objects.all()
    serializer_class = TestimonialSerializer
    ordering = ['-is_featured', 'order', '-created_at']

class FAQViewSet(viewsets.ReadOnlyModelViewSet):
    """API endpoint for retrieving FAQs."""
    queryset = FAQ.objects.filter(is_active=True)
    serializer_class = FAQSerializer
    ordering = ['category', 'order', 'created_at']


class PrivacyPolicyViewSet(viewsets.ReadOnlyModelViewSet):
    """API endpoint for retrieving privacy policy content."""
    queryset = PrivacyPolicy.objects.all()
    serializer_class = PrivacyPolicySerializer
    ordering = ['created_at']

class PricingPlanViewSet(viewsets.ReadOnlyModelViewSet):
    """API endpoint for retrieving pricing plans."""
    queryset = PricingPlan.objects.all()
    serializer_class = PricingPlanSerializer
    ordering = ['created_at']


class BlogPostViewSet(viewsets.ReadOnlyModelViewSet):
    """API endpoint for retrieving published blog posts."""
    queryset = BlogPost.objects.filter(is_published=True)
    serializer_class = BlogPostSerializer
    lookup_field = 'slug'
    ordering = ['-created_at']

    def get_object(self):
        queryset = self.get_queryset()
        lookup_url_kwarg = self.lookup_url_kwarg or self.lookup_field
        slug = self.kwargs[lookup_url_kwarg]
        return queryset.get(slug=slug)

class ContactMessageAPIView(APIView):
    def post(self, request):
        serializer = ContactMessageSerializer(data=request.data)

        if serializer.is_valid():
            contact = serializer.save()

            # Notify admin
            try:
                send_mail(
                    subject=f"New Contact Message: {contact.subject}",
                    message=f"From: {contact.full_name} ({contact.email})\n"
                            f"Company: {contact.company_name}\n"
                            f"Phone: {contact.phone}\n\n"
                            f"Message:\n{contact.message}",
                    from_email="info@partyfiy.com",
                    recipient_list=["info@partyfiy.com"],
                    fail_silently=False,
                )

                # Confirm receipt to user
                send_mail(
                    subject="We received your message!",
                    message=f"Hi {contact.full_name},\n\n"
                            f"Thanks for reaching out. We'll get back to you shortly.\n\n"
                            f"Your message:\n{contact.message}\n\n"
                            f"Best regards,\nPartyfiy Team",
                    from_email="info@partyfiy.com",
                    recipient_list=[contact.email],
                    fail_silently=False,
                )
            except Exception as e:
                return Response(
                        {"error": str(e)},
                        status=status.HTTP_500_INTERNAL_SERVER_ERROR
                    )
                # print(f"Email error: {e}")

            return Response(
                {"detail": "Your message has been sent successfully!"},
                status=status.HTTP_201_CREATED
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request):
        contacts = ContactMessage.objects.all().order_by('-created_at')
        serializer = ContactMessageSerializer(contacts, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

