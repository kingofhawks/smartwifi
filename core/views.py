from django.shortcuts import render

# Create your views here.
def dashboard(request, template="dashboard.html"):

    return render(request, template)
