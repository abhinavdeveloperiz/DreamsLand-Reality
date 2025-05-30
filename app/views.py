from django.shortcuts import render,redirect,get_object_or_404
from .models import Agent
from .forms import AgentUpdateForm

# Create your views here.


def Agent_profile(request):
    qs= Agent.objects.first()
    return render(request, 'agent_profile.html', {'qs': qs}) 

def Agent_update(request,id):
    qs=get_object_or_404(Agent, id=id)
    if request.method == 'POST':
        form= AgentUpdateForm(request.POST, request.FILES, instance=qs)
        if form.is_valid():
            form.save()
            return redirect('agent')
    else:
        form = AgentUpdateForm(instance=qs)
    return render(request, 'agent_update.html', {'form': form})



# views.py
import requests
from django.shortcuts import render, redirect
from django.http import HttpResponse

API_BASE_URL = "https://api-fxz7qcfy4q-uc.a.run.app"

# --- Preference Utilities ---
def set_pref(request, key, value):
    request.session[key] = value

def get_pref(request, key, default=None):
    return request.session.get(key, default)

# --- Agent Login ---
def agent_login(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")  # not used now, but stored

        if username and password:
            set_pref(request, "agent_username", username)
            set_pref(request, "agent_password", password)  # store if needed later
            return redirect("property_list")
        else:
            return HttpResponse("Username and password are required", status=400)

    return render(request, "agent_login.html")

# --- Property Listing ---
def property_list(request):
    agent_id = get_pref(request, "agent_username")
    if not agent_id:
        return redirect("agent_login")

    url = f"{API_BASE_URL}/{agent_id}/properties"
    try:
        response = requests.get(url)
        response.raise_for_status()
        properties = response.json()
    except requests.RequestException as e:
        print(f"Error fetching properties: {e}")
        properties = []

    return render(request, "properties_list.html", {"properties": properties,"agent":agent_id})






