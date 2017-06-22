from django import forms

from miner.data.cities_array import cities_choices


class DataFormForm(forms.Form):
    active_no = forms.CharField(required=False, initial="", max_length=256, label="Number")
    city_data_not_found = forms.BooleanField(required=False, initial=False, label="City data not found")
    city = forms.ChoiceField(required=True, choices=cities_choices, label="City")
    name = forms.CharField(required=False, max_length=256, label="Name (Company/Person)")
    dba = forms.CharField(required=False, max_length=256, label="DBA")
    phone = forms.CharField(required=False, max_length=256, label="Phone")
    carrier_type = forms.CharField(required=False, max_length=256, label="Carrier Type")
    active_trucks = forms.IntegerField(required=False, initial=0, label="Active Trucks")
    mailing_address = forms.CharField(required=False, initial="", max_length=256, widget=forms.Textarea(attrs={"rows": 2, "cols": 50}), label="Mailing Address")
    effective_date = forms.CharField(required=False, initial="", max_length=256, label="Effective Date")

    #
    checked_manually = forms.BooleanField(required=False, initial=False, label="Checked Manually?")

    data_id = forms.IntegerField(required=False, widget=forms.HiddenInput)
