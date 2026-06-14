from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def content_view(request):
    # return render(request, 'content/content.html')
    return HttpResponse("Welcome to the Content Page!")