import requests
from django.shortcuts import redirect, render
from .models import City
from .forms import CityForm

# Create your views here.
def index(request):
    url = "http://api.openweathermap.org/data/2.5/weather?q={}&units=metric&appid=ca4ff4bfaeddc517d3fa9bbcb2e70ce2"

    err_msg=''
    message=''
    message_class=''

    if request.method == "POST":
        form = CityForm(request.POST)

        if form.is_valid():
            new_city=form.cleaned_data['name']
            existing_city_count=City.objects.filter(name=new_city).count()
            if existing_city_count==0:
                r = requests.get(url.format(new_city)).json() 
                if r['cod']==200:
                    form.save()
                else:
                    err_msg="City does not exist in the world!!"
                
           
        if err_msg:
            message=err_msg
            message_class='is-danger'
        

    form = CityForm()

    cities = City.objects.all()
    weather_data = []


    for city in cities:
        r = requests.get(url.format(city)).json()

        city_weather = {
        "city": city.name,
        "temperature": r["main"]["temp"], 
        "description": r["weather"][0]["description"],
        "icon": r["weather"][0]["icon"],
        }
        
        weather_data.append(city_weather)



    context = {
        "weather_data": weather_data, 
        "form": form,
        "message":message,
        "message_class": message_class
    }
    return render(request, "home.html", context)


def delete_city(request,city_name):
    City.objects.get(name=city_name).delete()
    return redirect('home')

def delete_everything(request):
    cities = City.objects.all()
    for city in cities:
        City.objects.get(name=city).delete()
    return redirect('home')
