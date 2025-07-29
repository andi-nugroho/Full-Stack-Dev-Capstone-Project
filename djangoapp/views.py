from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import AuthenticationForm
from .forms import RegistrationForm
import requests
import json
# Anda mungkin perlu menginstal ibm-watson: pip install ibm-watson
from ibm_watson import NaturalLanguageUnderstandingV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator

# ... (kode login, logout, registration tidak berubah) ...

def login_request(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('djangoapp:index')
    form = AuthenticationForm()
    return render(request, 'djangoapp/login.html', {'form': form})

def logout_request(request):
    logout(request)
    return redirect('djangoapp:index')

def registration_request(request):
    if request.method == "POST":
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('djangoapp:index')
    else:
        form = RegistrationForm()
    return render(request, 'djangoapp/registration.html', {'form': form})

# View untuk halaman utama dengan filter state
def get_dealerships(request):
    url = "http://localhost:3000/api/dealership"
    try:
        # Selalu ambil semua dealer dulu untuk mendapatkan daftar state
        response_all = requests.get(url)
        all_dealerships = response_all.json() if response_all.status_code == 200 else []
        all_states = sorted(list(set(d['st'] for d in all_dealerships)))

        # Filter jika ada parameter state di URL
        state = request.GET.get('state')
        if state:
            url += f"?state={state}"

        response_filtered = requests.get(url)
        dealerships = response_filtered.json() if response_filtered.status_code == 200 else []

    except requests.exceptions.RequestException:
        dealerships = []
        all_states = []

    context = {'dealerships': dealerships, 'all_states': all_states}
    return render(request, 'djangoapp/index.html', context)

# ... (kode get_dealer_details tidak berubah) ...
def get_dealer_details(request, dealer_id):
    context = {}
    try:
        response_dealer = requests.get(f'http://localhost:3000/api/dealership?id={dealer_id}')
        if response_dealer.status_code == 200:
            context['dealer'] = response_dealer.json()[0]
        response_reviews = requests.get(f'http://localhost:3000/api/review?dealerId={dealer_id}')
        if response_reviews.status_code == 200:
            context['reviews'] = response_reviews.json()
    except:
        print("Network error or API is down.")
    return render(request, 'djangoapp/dealer_details.html', context)

# ... (kode add_review tidak berubah) ...
def add_review(request, dealer_id):
    if request.method == "POST":
        data = { "dealerId": dealer_id, "name": request.POST.get('name'), "review": request.POST.get('review'), "purchase": request.POST.get('purchase') == 'on', "purchase_date": request.POST.get('purchase_date') }
        try:
            response = requests.post('http://localhost:3000/api/review', json=data)
            if response.status_code == 201:
                return redirect('djangoapp:dealer_details', dealer_id=dealer_id)
        except:
            print("Network error or API is down.")
    try:
        response = requests.get(f'http://localhost:3000/api/dealership?id={dealer_id}')
        dealer_name = response.json()[0]['name'] if response.status_code == 200 else "Dealer"
    except:
        dealer_name = "Dealer"
    context = {'dealer_id': dealer_id, 'dealer_name': dealer_name}
    return render(request, 'djangoapp/add_review.html', context)

# ... (kode about dan contact tidak berubah) ...
def about(request):
    return render(request, 'djangoapp/about.html')

def contact(request):
    return render(request, 'djangoapp/contact.html')

# View BARU untuk Sentiment Analyzer
def sentiment_analyzer(request):
    text_to_analyze = request.GET.get('text', '')
    # GANTI DENGAN URL & API_KEY ANDA
    url = "URL_LAYANAN_NLU_ANDA"
    api_key = "API_KEY_ANDA"

    try:
        authenticator = IAMAuthenticator(api_key)
        nlu = NaturalLanguageUnderstandingV1(version='2022-04-07', authenticator=authenticator)
        nlu.set_service_url(url)
        response = nlu.analyze(text=text_to_analyze, features={'sentiment': {}}).get_result()
        sentiment = response['sentiment']['document']['label']
    except Exception as e:
        print(f"Error analyzing sentiment: {e}")
        sentiment = "neutral"

    return JsonResponse({"sentiment": sentiment})