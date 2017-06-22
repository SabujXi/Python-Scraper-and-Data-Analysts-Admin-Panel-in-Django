from django.contrib import messages
from django.shortcuts import render, redirect
# Create your views here.
from django.views import View

from data.forms import DataFormForm
from data.models import DataModel


def index(request):
    return render(request, "index.html")


class DataFormView(View):
    template = "data_form.html"

    def get(self, request, data_id=""):
        city = ""
        if data_id:
            d = DataModel.objects.get(pk=int(data_id))
            city = d.city
            form = DataFormForm(initial={
                "active_no": d.active_no,
                "city_data_not_found" : d.city_data_not_found,
                "city": d.city,
                "name": d.name,
                "dba": d.city,
                "phone": d.phone,
                "carrier_type": d.carrier_type,
                "active_trucks": d.active_trucks,
                "mailing_address": d.mailing_address,
                "effective_date": d.effective_date,
                "checked_manually": d.checked_manually,
                "data_id": d.id
            })
            active_no = d.active_no
        else:
            form = DataFormForm()
            active_no = ""
        return render(request, self.template, context={
            "form": form,
            "city": city,
            "data_id": data_id,
            "active_no": active_no
        })

    def post(self, request, **kwargs):
        form = DataFormForm(request.POST)
        if form.is_valid():
            d = form.cleaned_data
            data_id = d['data_id']
            if data_id == "" or data_id is None:
                # New
                data = DataModel()
            else:
                # Save
                data = DataModel.objects.get(pk=data_id)

            data.active_no = d["active_no"]
            data.city_data_not_found = d["city_data_not_found"]
            data.city = d["city"]
            data.name = d["name"]
            data.dba = d["dba"]
            data.phone = d["phone"]
            data.carrier_type = d["carrier_type"]
            data.active_trucks = d["active_trucks"]
            data.mailing_address = d["mailing_address"]
            data.effective_date = d["effective_date"]
            data.checked_manually = d["checked_manually"]
            data.save()
            data_id = data.id
            messages.info(request, "Data successfully saved")
            return redirect("data:data_form", data_id=data_id)

        else:
            messages.warning(request, "ERROR in the form")
            return render(request, self.template, context={
                "form": form,
                "city": request.POST['city'],
                "data_id": request.POST['data_id'],
                "active_no": request.POST.get("active_no", "")
            })


def list_data(request, city):
    data_by_c = DataModel.objects.all().filter(city__iexact=city)
    # data_by_c.sort()
    return render(request, "data_list.html", context={
        "data_s": data_by_c,
        "city": city
    })


def list_city_found(request):
    a = DataModel.objects.filter(city_data_not_found=False)
    cities = set()
    for d in a:
        cities.add(d.city)

    cities_s = list(cities)
    cities_s.sort()

    return render(request, "list_city.html", context={
        "cities": cities_s
    })


def list_city_not_found(request):
    a = DataModel.objects.filter(city_data_not_found=True)
    cities = set()
    for d in a:
        cities.add(d.city)
    cities_s = list(cities)
    cities_s.sort()
    return render(request, "list_city.html", context={
        "cities": cities_s
    })


def delete_data(request, data_id):
    d = DataModel.objects.get(pk=int(data_id))
    id = d.id
    d.delete()
    messages.info(request, "successfully deleted data id: %s " % id)
    return redirect(request.META['HTTP_REFERER'])

def different_data_list(request):
    pass

def different_data_compare(request):
    pass

def different_data_merge(request):
    pass