from django import forms
from .cities_array import cities_choices


class DataFormForm(forms.Form):
    active_no = forms.CharField(required=True, max_length=256, label="Number")
    city_data_not_found = forms.BooleanField(initial=False, label="City data not found")
    city = forms.ChoiceField(max_length=256, db_index=True, choices=cities_choices, label="City")
    name = forms.CharField(max_length=256, label="Name (Company/Person)")
    dba = forms.CharField(max_length=256, label="DBA")
    phone = forms.CharField(max_length=256, label="Phone")
    carrier_type = forms.CharField(max_length=256, label="Carrier Type")
    active_trucks = forms.IntegerField(label="Active Trucks")
    mailing_address = forms.CharField(max_length=256, widget=forms.Textarea, label="Mailing Address")
    effective_date = forms.CharField(max_length=256, label="Effective Date")

    #
    checked_manually = forms.BooleanField(initial=False, label="Checked Manually?")
