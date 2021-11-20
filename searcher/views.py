from django.shortcuts import render, redirect
from .services import storage, auth


# Create your views here.
def index(request):
    return render(request, 'searcher/index.html')


def integrate(request):
    client_data = storage.load_client_data()
    client_data["authorization_code"] = request.GET["code"]
    new_client_data = client_data
    storage.save_client_data(new_client_data)
    auth.create_initial_tokens(new_client_data)

    return redirect('index')
