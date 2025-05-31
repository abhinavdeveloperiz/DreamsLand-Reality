from django.shortcuts import render,redirect,get_object_or_404
from .models import Agent
from .forms import AgentUpdateForm
from django.contrib import messages
from django.http import HttpResponse
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

def agent_logout(request):
    """Logs out the agent by clearing session preferences."""
    request.session.flush()  # Clear all session data
    return redirect("agent_login")  # Redirect to login page after logout



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
        password = request.POST.get("password")

        if username and password:
            set_pref(request, "agent_username", username)
            set_pref(request, "agent_password", password)
            return redirect("property_list")
        else:
            return HttpResponse("Username and password are required", status=400)

    return render(request, "agent_login.html")

def agent_logout(request):
    request.session.flush()
    return redirect("agent_login")

# --- Property List View ---
def property_list(request):
    agent_id = get_pref(request, "agent_username")
    if not agent_id:
        return redirect("agent_login")

    url = f"{API_BASE_URL}/{agent_id}/properties"
    try:
        response = requests.get(url)
        response.raise_for_status()
        properties_raw = response.json()

        properties = []
        for prop in properties_raw:
            # Extract actual MongoDB $oid
            if isinstance(prop.get('_id'), dict):
                prop['id'] = prop['_id'].get('$oid', '')
            else:
                prop['id'] = prop.get('_id', '')  # fallback
            properties.append(prop)

    except requests.RequestException as e:
        print(f"Error fetching properties: {e}")
        properties = []

    return render(request, "properties_list.html", {"properties": properties, "agent": agent_id})

# --- Property Update View ---
def property_update(request, id):
    # Get agent credentials from session
    agent_id = get_pref(request, "agent_username")
    if not agent_id:
        return redirect("agent_login")

    # Direct property URL without agent ID
    property_url = f"{API_BASE_URL}/property/{id}"

    try:
        # Fetch current property data
        response = requests.get(property_url)
        response.raise_for_status()
        property_data = response.json()
        
    except requests.RequestException as e:
        print(f"Error fetching property: {e}")
        messages.error(request, f"Failed to fetch property: {e}")
        return redirect("property_list")

    if request.method == "POST":
        # Prepare update data
        update_data = {
            "location": request.POST.get("location"),
            "name": request.POST.get("name"),
            "type": request.POST.get("type"),
            "subtype": request.POST.get("subtype"),
            "bhk": int(request.POST.get("bhk", 0)),
            "sqft": request.POST.get("sqft"),
            "price": int(request.POST.get("price", 0)),
            "plotArea": request.POST.get("plotArea"),
            "unit": request.POST.get("unit"),
            "status": request.POST.get("status"),
            "propertyDescription": request.POST.get("propertyDescription"),
            "ownerName": request.POST.get("ownerName"),
            "phoneNumber": request.POST.get("phoneNumber"),
            "whatsappNumber": request.POST.get("whatsappNumber")
        }

        try:
            # Send PUT request to update property
            update_response = requests.put(
                property_url,
                json=update_data,
                headers={"Content-Type": "application/json"}
            )
            update_response.raise_for_status()
            messages.success(request, "Property updated successfully")
            return redirect("property_list")
            
        except requests.RequestException as e:
            print(f"Error updating property: {e}")
            messages.error(request, f"Failed to update property: {e}")
            return render(request, "property_update.html", {"property": property_data})

    return render(request, "property_update.html", {"property": property_data})

