from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth import authenticate, login
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import LoginForm
from django.contrib.auth import login as auth_login, logout
from dashboard.models import *

from django.core.mail import send_mail
from django.conf import settings

# Create your views here.
@login_required
def dashboard_view(request):
    testmionials_count = Testimonial.objects.count()
    blog_posts_count = BlogPost.objects.count()
    features_count = Feature.objects.count()
    faq_count = FAQ.objects.count()
    
    return render(request, 'dashboard/index.html', {
        'testimonials_count': testmionials_count,
        'blog_posts_count': blog_posts_count,
        'features_count': features_count,
        'faq_count': faq_count
    })
    # return HttpResponse("Welcome to the Dashboard!")


# def login_view(request):
#     if request.user.is_authenticated:
#         return redirect("dashboard")

#     if request.method == "POST":
#         print(request.POST)

#         username = request.POST.get("username")
#         password = request.POST.get("password")

#         user = authenticate(
#             request,
#             username=username,
#             password=password
#         )

#         print(username)
#         print(password)

#         print("USER:", user)

#         if user is not None:
#             login(request, user)
#             return redirect("dashboard")
        
#         messages.error(request, "Invalid username or password")

#         return render(
#             request, 
#             "dashboard/login.html",
#             {"error": "Invalid username or password"}
#         )

#     return render(request, "dashboard/login.html", )



def login(request):
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            auth_login(request, user)
            # # Redirect to the appropriate page after login
            return redirect('dashboard:dashboard')  # Adjust the redirect URL as needed
        else:
            messages.warning(request, 'Username Or password is incorrect')

    else:
        form = LoginForm()

    return render(request, 'dashboard/login.html', {'form': form})


@login_required
def logout_view(request):
    logout(request)
    return redirect('dashboard:login')

# @login_required
# def testimonials_view(request):
#     testimonials = Testimonial.objects.all()
#     return render(request, 'dashboard/testimonials.html', {'testimonials': testimonials})



from django.shortcuts import render, redirect, get_object_or_404
from .models import Testimonial

@login_required
def testimonials_view(request):
    if request.method == "POST":
        action = request.POST.get("action")

        if action == "create":
            Testimonial.objects.create(
                client_name=request.POST.get("client_name"),
                client_title=request.POST.get("client_title"),
                client_company=request.POST.get("client_company"),
                client_image=request.FILES.get("client_image"),
                content=request.POST.get("content"),
                rating=request.POST.get("rating"),
                # order=request.POST.get("order") or 0,
            )

        elif action == "update":
            testimonial = get_object_or_404(
                Testimonial,
                id=request.POST.get("testimonial_id")
            )
            testimonial.client_name = request.POST.get("client_name")
            testimonial.client_title = request.POST.get("client_title")
            testimonial.client_company = request.POST.get("client_company")
            testimonial.client_image = request.POST.get("client_image")
            testimonial.content = request.POST.get("content")
            testimonial.rating = request.POST.get("rating")
            # testimonial.order = request.POST.get("order") or 0
            
            if request.FILES.get("client_image"):
                testimonial.client_image = request.FILES.get("client_image")

            testimonial.save()

        elif action == "delete":
            testimonial = get_object_or_404(
                Testimonial,
                id=request.POST.get("testimonial_id")
            )
            testimonial.delete()

        return redirect("dashboard:testimonials")

    testimonials = Testimonial.objects.all()

    return render(
        request,
        "dashboard/testimonials.html",
        {"testimonials": testimonials}
    )


def blog_view(request):
    if request.method == "POST":
        action = request.POST.get("action")
        category_id = request.POST.get("category")

        if action == "create":
            BlogPost.objects.create(
                title=request.POST.get("title"),
                slug=request.POST.get("slug"),
                # category=request.POST.get("category"),
                category_id=category_id if category_id else None,
                author=request.POST.get("author"),
                content=request.POST.get("content"),
                is_published="is_published" in request.POST,
                image=request.FILES.get("image"),
                views=request.POST.get("views") or 0,
            )
        
        elif action == "update":
            blog_post = get_object_or_404(
                BlogPost,
                id=request.POST.get("blog_id")
            )
            blog_post.title = request.POST.get("title")
            blog_post.slug = request.POST.get("slug")
            # blog_post.category = request.POST.get("category")
            blog_post.category_id = request.POST.get("category") or None
            blog_post.author = request.POST.get("author")
            blog_post.content = request.POST.get("content")
            blog_post.is_published = "is_published" in request.POST
            blog_post.views = request.POST.get("views") or 0
            
            if request.FILES.get("image"):
                blog_post.image = request.FILES.get("image")

            blog_post.save()

        elif action == "delete":
            blog_post = get_object_or_404(
                BlogPost,
                id=request.POST.get("blog_id")
            )
            blog_post.delete()

        return redirect("dashboard:blog")

    blog_posts = BlogPost.objects.all()
    categories = BlogCategory.objects.all()

    return render(
        request,
        "dashboard/blog.html",
        {"blog_posts": blog_posts, "categories": categories}
    )


@login_required
def faq_view(request):
    if request.method == "POST":
        action = request.POST.get("action")

        if action == "create":
            FAQ.objects.create(
                question=request.POST.get("question"),
                answer=request.POST.get("answer"),
                # is_active=request.POST.get("is_active") == "on"
                is_active="is_active" in request.POST
                # is_active = request.POST.get("is_active") == "true"
            )

        elif action == "update":
            faq = get_object_or_404(
                FAQ,
                id=request.POST.get("faq_id")
            )
            faq.question = request.POST.get("question")
            faq.answer = request.POST.get("answer")
            # faq.is_active = request.POST.get("is_active") == "on"
            faq.is_active = "is_active" in request.POST
            faq.save()

        elif action == "delete":
            faq = get_object_or_404(
                FAQ,
                id=request.POST.get("faq_id")
            )
            faq.delete()

        return redirect("dashboard:faq")
    faqs = FAQ.objects.all()
    return render(request, 'dashboard/faq.html', {'faqs': faqs})



@login_required
def features_view(request):
    if request.method == "POST":
        action = request.POST.get("action")

        if action == "create":
            Feature.objects.create(
                title=request.POST.get("title"),
                image=request.FILES.get("image"),
                description=request.POST.get("description"),
                # order=request.POST.get("order") or 0,
                is_active="is_active" in request.POST
            )

        elif action == "update":
            feature = get_object_or_404(
                Feature,
                id=request.POST.get("feature_id")
            )
            feature.title = request.POST.get("title")
            feature.description = request.POST.get("description")
            feature.is_active = "is_active" in request.POST
            # feature.order = request.POST.get("order") or 0
            
            if request.FILES.get("image"):
                feature.image = request.FILES.get("image")

            feature.save()

        elif action == "delete":
            feature = get_object_or_404(
                Feature,
                id=request.POST.get("feature_id")
            )
            feature.delete()

        return redirect("dashboard:features")

    features = Feature.objects.all()

    return render(
        request,
        "dashboard/features.html",
        {"features": features}
    )

@login_required
def privacy_view(request):
    if request.method == "POST":
        action = request.POST.get("action")

        if action == "create":
            PrivacyPolicy.objects.create(
                title=request.POST.get("title"),
                content=request.POST.get("content"),
            )

        elif action == "update":
            policy = get_object_or_404(
                PrivacyPolicy,
                id=request.POST.get("policy_id")
            )
            policy.title = request.POST.get("title")
            policy.content = request.POST.get("content")
            policy.save()
        
        elif action == "delete":
            policy = get_object_or_404(
                PrivacyPolicy,
                id=request.POST.get("policy_id")
            )
            policy.delete()

        
        return redirect("dashboard:privacy")
    
    privacy = PrivacyPolicy.objects.all()

    return render(
        request,
        "dashboard/privacy.html",
        {"privacy": privacy}
    )


@login_required
def blog_category_view(request):
    if request.method == "POST":
        action = request.POST.get("action")

        if action == "create":
            BlogCategory.objects.create(
                title=request.POST.get("title"),
                description=request.POST.get("description"),
            )

        elif action == "update":
            category = get_object_or_404(
                BlogCategory,
                id=request.POST.get("blog_category_id")
            )
            category.title = request.POST.get("title")
            category.description = request.POST.get("description")
            category.save()

        elif action == "delete":
            category = get_object_or_404(
                BlogCategory,
                id=request.POST.get("category_id")
            )
            category.delete()

        return redirect("dashboard:blog_category")

    categories = BlogCategory.objects.all()

    return render(
        request,
        "dashboard/blog_category.html",
        {"categories": categories}
    )


@login_required
def contact_view(request):
    if request.method == "POST":
        ContactMessage.objects.create(
            full_name=request.POST.get("full_name"),
            company_name=request.POST.get("company_name"),
            email=request.POST.get("email"),
            phone=request.POST.get("phone"),
            subject=request.POST.get("subject"),
            message=request.POST.get("message")
        )

        messages.success(request, "Your message has been sent successfully!")

        return redirect("dashboard:contact")

    return render(request, 'dashboard/contact.html')



from django.core.mail import send_mail
from django.conf import settings


@login_required
def contact_view(request):
    if request.method == "POST":
        full_name = request.POST.get("full_name")
        company_name = request.POST.get("company_name")
        email = request.POST.get("email")
        phone = request.POST.get("phone")
        subject = request.POST.get("subject")
        message = request.POST.get("message")

        ContactMessage.objects.create(
            full_name=full_name,
            company_name=company_name,
            email=email,
            phone=phone,
            subject=subject,
            message=message
        )

        # Email 1 — Notify admin of new contact message
        send_mail(
            subject=f"New Contact Message: {subject}",
            message=f"From: {full_name} ({email})\n"
                    f"Company: {company_name}\n"
                    f"Phone: {phone}\n\n"
                    f"Message:\n{message}",
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[settings.ADMIN_EMAIL],
        )

        # Email 2 — Confirm receipt to the user
        send_mail(
            subject="We received your message!",
            message=f"Hi {full_name},\n\n"
                    f"Thanks for reaching out. We've received your message and will get back to you shortly.\n\n"
                    f"Your message:\n{message}\n\n"
                    f"Best regards,\nYour Team",
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[email],
        )

        messages.success(request, "Your message has been sent successfully!")
        return redirect("dashboard:contact")

    return render(request, 'dashboard/contact.html')




def featurepricing_view(request):
    if request.method == "POST":
        action = request.POST.get("action")

        if action == "create":
            FeaturePricing.objects.create(
                title=request.POST.get("title"),
                description=request.POST.get("description"),
                is_active="is_active" in request.POST,
            )

        elif action == "update":
            feature = get_object_or_404(
                FeaturePricing,
                id=request.POST.get("feature_id")
            )

            feature.title = request.POST.get("title")
            feature.description = request.POST.get("description")
            feature.is_active = "is_active" in request.POST
            feature.save()

        elif action == "delete":
            feature = get_object_or_404(
                FeaturePricing,
                id=request.POST.get("feature_id")
            )

            feature.delete()

        return redirect("dashboard:pricing-features")

    features = FeaturePricing.objects.all()

    return render(
        request,
        "dashboard/features-pricing.html",
        {"features": features}
    )


def pricing_view(request):
    if request.method == "POST":
        action = request.POST.get("action")

        if action == "create":
            plan = PricingPlan.objects.create(
                name=request.POST.get("name"),
                description=request.POST.get("description"),
                price=request.POST.get("price"),
                # billing_period=request.POST.get("billing_period"),
                # display_order=request.POST.get("display_order") or 0,
                is_active="is_active" in request.POST,
            )

            plan.features.set(
                request.POST.getlist("features")
            )

        elif action == "update":
            plan = get_object_or_404(
                PricingPlan,
                id=request.POST.get("plan_id")
            )

            plan.name = request.POST.get("name")
            plan.description = request.POST.get("description")
            plan.price = request.POST.get("price")
            # plan.billing_period = request.POST.get("billing_period")
            # plan.display_order = request.POST.get("display_order") or 0
            plan.is_active = "is_active" in request.POST

            plan.save()

            plan.features.set(
                request.POST.getlist("features")
            )

        elif action == "delete":
            plan = get_object_or_404(
                PricingPlan,
                id=request.POST.get("plan_id")
            )

            plan.delete()

        return redirect("dashboard:pricing")

    plans = PricingPlan.objects.prefetch_related("features")
    features = FeaturePricing.objects.filter(is_active=True)

    return render(
        request,
        "dashboard/pricing.html",
        {
            "plans": plans,
            "features": features,
        }
    )