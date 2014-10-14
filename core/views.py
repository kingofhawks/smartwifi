from django.shortcuts import render


def index(request):
    return render(request, 'index.html')

# Create your views here.
def dashboard(request, template="dashboard.html"):

    return render(request, template)
