from django.db import models
from django.conf import settings
from django.utils.text import slugify
# from cloudinary_storage.storage import MediaCloudinaryStorage


# Create your models here.

class SiteSettings(models.Model):
    site_name = models.CharField(max_length=200)
    contact_email = models.EmailField(default="info@partyfiy.com")
    phone = models.CharField(max_length=30)
    address = models.TextField()
    privacy_policy = models.TextField(blank=True)

    def __str__(self):
        return self.site_name


class FAQ(models.Model):
    question = models.CharField(max_length=255)
    answer = models.TextField()
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['question', 'created_at']
        verbose_name = 'FAQ'
        verbose_name_plural = 'FAQs'
 
    def __str__(self):
        return self.question
    

class Testimonial(models.Model):
    client_name = models.CharField(max_length=200)
    client_title = models.CharField(max_length=200, blank=True)
    client_company = models.CharField(max_length=200, blank=True)
    # client_image = models.ImageField(upload_to='testimonials/', storage=MediaCloudinaryStorage() , blank=True, null=True)
    client_image = models.ImageField(upload_to='testimonials/', blank=True, null=True)
    content = models.TextField()
    rating = models.IntegerField(default=5, choices=[(i, str(i)) for i in range(1, 6)])
    order = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['client_name', '-created_at']
        verbose_name = 'Testimonial'
        verbose_name_plural = 'Testimonials'

    def __str__(self):
        return f"Testimonial from {self.client_name}"


class Feature(models.Model):
    title = models.CharField(max_length=200)
    # image = models.ImageField(upload_to='features/', storage=MediaCloudinaryStorage() , blank=True, null=True)
    image = models.ImageField(upload_to='features/', blank=True, null=True)
    description = models.TextField()
    order = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['order', 'created_at']
        verbose_name = 'Feature'
        verbose_name_plural = 'Features'
 
    def __str__(self):
        return self.title


class ContactMessage(models.Model):
    full_name = models.CharField(max_length=200)
    company_name = models.CharField(max_length=200, blank=True)
    email = models.EmailField()
    subject = models.CharField(max_length=300)
    phone = models.CharField(max_length=50, blank=True)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Contact Message'
        verbose_name_plural = 'Contact Messages'
 
    def __str__(self):
        return f"{self.name} – {self.subject or 'No subject'} ({self.created_at.strftime('%Y-%m-%d')})"
    

class PrivacyPolicy(models.Model):
    """Privacy policy page content."""
    title = models.CharField(max_length=300, default='Privacy Policy')
    content = models.TextField()
    last_updated = models.DateTimeField(auto_now_add=True)
    effective_date = models.DateField(null=True, blank=True)

    class Meta:
        verbose_name = 'Privacy Policy'
        verbose_name_plural = 'Privacy Policies'

    def __str__(self):
        return self.title

    @classmethod
    def get_policy(cls):
        """Get the current privacy policy."""
        return cls.objects.first()


class BlogCategory(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class BlogPost(models.Model):
    title = models.CharField(max_length=300, unique=True)
    slug = models.SlugField(max_length=300, unique=True)
    author = models.CharField(max_length=100, default='Partyfiy Team')
    # category = models.CharField(max_length=100, blank=True)
    content = models.TextField()
    is_published = models.BooleanField(default=True)
    # image = models.ImageField(upload_to='blog-posts/', storage=MediaCloudinaryStorage() , blank=True, null=True)
    image = models.ImageField(upload_to='blog/', blank=True, null=True)
    views = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now= True)
    category = models.ForeignKey(BlogCategory, null=True, blank=True, on_delete=models.CASCADE)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Blog Post'
        verbose_name_plural = 'Blog Posts'
        indexes = [
            models.Index(fields=['-created_at']),
            models.Index(fields=['is_published']),
        ]

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)



class FeaturePricing(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
    

class PricingPlan(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    # billing_period = models.CharField(
    #     max_length=20,
    #     choices=[
    #         ("monthly", "Monthly"),
    #         ("yearly", "Yearly"),
    #         ("one-time", "One Time"),
    #     ],
    #     default="monthly"
    # )
    features = models.ManyToManyField(
        FeaturePricing,
        blank=True,
        related_name="plans"
    )
    is_active = models.BooleanField(default=True)
    # display_order = models.PositiveIntegerField(default=0)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name

# class PricingPlan(models.Model):
#     name = models.CharField(max_length=100)
#     price = models.DecimalField(max_digits=10,decimal_places=2)
#     currency = models.CharField(max_length=3,default="USD")
#     billing_period = models.CharField(max_length=50,default="month")
#     description = models.TextField(blank=True)
#     features = models.TextField(help_text="One feature per line")
#     button_text = models.CharField(max_length=100,default="Get Started")
#     is_active = models.BooleanField(default=True)
#     order = models.PositiveIntegerField(default=0)
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)

#     class Meta:
#         ordering = ["order", "created_at"]

#     def __str__(self):
#         return self.name