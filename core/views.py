from django.shortcuts import render
from accounts.models import Agent, Customer
from management.models import Gateway, WifiClient


def index(request):
    return render(request, 'index.html')


# Create your views here.
def dashboard(request, template="dashboard.html"):
    agent_count = Agent.objects.count()
    customer_count = Customer.objects.count()
    gateway_count = Gateway.objects.count()
    client_count = WifiClient.objects.count()

    return render(request, template, {'agent_count': agent_count, 'customer_count': customer_count,
                                      'gateway_count': gateway_count, 'client_count': client_count})
