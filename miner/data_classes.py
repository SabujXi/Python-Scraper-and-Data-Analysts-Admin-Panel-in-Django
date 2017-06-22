from .functions import clean_mailing_address


class CitySearchDict:
    req_dict = {
        "searchtype": "city",
        "citydata": "----",
        "city_status": "A",
        "city_carrier_type": "tow",
        "namedata": "",
        "name_carrier_type": "COMPANY",
        "mcrdata": "",
        "zipcodedata": "",
        "zip_status": "ALL",
        "zip_carrier_type": "all",
        "proc": ""
    }

    def __init__(self, city=""):
        self.city = city

    def get_data(self):
        d = self.req_dict.copy()
        d["citydata"] = self.city
        return d


class CustomerDataFromHTMLSource:
    def __init__(self):
        self.active_no = None
        self.city_data_not_found = False
        self.city = ""
        self.name = ""
        self.dba = ""
        self.phone = ""
        self.carrier_type = ""
        self.active_trucks = -1
        self.mailing_address = ""
        self.effective_date = ""
        #
        self.checked_manually = False

    def set_active_no(self, active_no):
        if active_no:
            active_no = active_no[0].strip()
        else:
            active_no = ""
        self.active_no = active_no

    def get_active_no(self):
        return self.active_no

    def set_city_data_not_found(self, cn):
        self.city_data_not_found = cn

    def get_city_data_not_found(self):
        return self.city_data_not_found

    def set_city(self, c):
        self.city = c

    def get_city(self):
        return self.city

    def set_name(self, name):
        if name:
            name = name[0].strip()
        else:
            name = ""
        self.name = name

    def get_name(self):
        return self.name

    def set_dba(self, dba):
        if not dba:
            dba = "NO DATA"
        else:
            dba = dba[0].strip()
        self.dba = dba

    def get_dba(self):
        return self.dba

    def set_phone(self, phone):
        if phone:
            phone = phone[0].strip()
        else:
            phone = ""
        self.phone = phone

    def get_phone(self):
        return self.phone

    def set_carrier_type(self, carrier_type):
        if carrier_type:
            carrier_type = carrier_type[0].strip()
        else:
            carrier_type = ""
        self.carrier_type = carrier_type

    def get_carrier_type(self):
        return self.carrier_type

    def set_active_trucks(self, active_trucks):
        if active_trucks:
            active_trucks = int(active_trucks[0].strip())
        else:
            active_trucks = -1
        self.active_trucks = active_trucks

    def get_active_trucks(self):
        if self.get_city_data_not_found():
            return 0
        else:
            return self.active_trucks

    def set_mailing_address(self, mailing_address):
        if mailing_address:
            mailing_address = clean_mailing_address(mailing_address)
        else:
            mailing_address = ""
        self.mailing_address = mailing_address

    def get_mailing_address(self):
        return self.mailing_address

    def set_effective_date(self, ed):
        self.effective_date = ed

    def get_effective_date(self):
        return self.effective_date

    def set_checked_manually(self, c):
        self.checked_manually = c

    def get_checked_manually(self):
        return self.checked_manually

    def get_record_url(self):
        if self.get_city_data_not_found():
            return None
        else:
            return "https://www.tdlr.texas.gov/tools_search/mccs_display.asp?mcrnumber=" + self.get_active_no()

    def save_to_model(self, instance):
        d = instance
        d.city = self.get_city()
        d.name = self.get_name()
        d.dba = self.get_dba()
        d.phone = self.get_phone()
        d.carrier_type = self.get_carrier_type()
        d.active_trucks = self.get_active_trucks()
        d.mailing_address = self.get_mailing_address()
        d.effective_date = self.get_effective_date()
        d.active_no = self.get_active_no()
        d.record_url = self.get_record_url()
        d.save()

    def save_to_csv(self, csvwriter, csvfile):
        if self.get_city_data_not_found():
            data_array = [self.get_city(), "*** City Data Not Found ***"]
        else:
            data_array = [self.get_city(),
                          self.get_name(),
                          self.get_dba(),
                          self.get_phone(),
                          self.get_carrier_type(),
                          self.get_active_trucks(),
                          self.get_mailing_address(),
                          self.get_effective_date(),
                          self.get_active_no()]
        csvwriter.writerow(data_array)
        csvfile.flush()

    def print_data(self):
        if self.get_city_data_not_found():
            print("%s " % self.get_city(), "city data was not found.")
        else:
            print("DBA: ", self.get_dba())
            print("Name: ", self.get_name())
            print("Phone: ", self.get_phone())
            print("Carrier Type: ", self.get_carrier_type())
            print("Active Trucks: ", self.get_active_trucks())
            print("Mailing address: ", self.get_mailing_address())
            print("Active Number: ", self.get_active_no())
            print("Effective date: ", self.get_effective_date())
            print("\n\n")