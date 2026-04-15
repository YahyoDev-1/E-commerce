from django.shortcuts import render
from django.views import View

# Create your views here.

class HomePageView(View):
    def get(self, request):
        if request.user.is_authenticated:
            return render(request, 'index.html')
        return render(request, 'index-without-auth.html')