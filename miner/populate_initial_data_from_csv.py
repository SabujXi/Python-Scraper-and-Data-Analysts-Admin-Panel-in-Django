import sys, os.path
root_dir = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
sys.path.append(root_dir)
print(root_dir)
import csv

from data.models import DataModel

with open("data/data.csv", newline='') as cr:
    csvreader = csv.reader(cr)
    idx = 0
    for row in csvreader:
        if idx == 0:
            idx += 1
            continue
        idx += 1

        datamodel = DataModel()
        if len(row) == 2:
            city = row[0]
            # print(city, " NOT found")
            datamodel.city = city
            datamodel.city_data_not_found = True
            datamodel.save()

        elif len(row) == 9:
            city = row[0]
            name = row[1]
            dba = row[2]
            phone = row[3]
            carrier_type = row[4]
            active_trucks = row[5]
            mailing_address = row[6]
            effective_date = row[7]
            active_no = row[8]
            # print(active_trucks)
            if not active_trucks.isdigit():
                print("-++++++++ active trucks is not digit: %s" % active_trucks)

            if active_trucks == "":
                print("-++++++++ active trucks is empty")
                active_trucks = "-1"

            d = datamodel
            d.city = city
            d.name = name
            d.dba = dba
            d.phone = phone
            d.carrier_type = carrier_type
            d.active_trucks = int(active_trucks)
            d.mailing_address = mailing_address.strip()
            d.effective_date = effective_date
            d.active_no = active_no
            d.record_url = "https://www.tdlr.texas.gov/tools_search/mccs_display.asp?mcrnumber=" + active_no
            d.save()

        else:
            print("Row length did not match\n" * 100)
