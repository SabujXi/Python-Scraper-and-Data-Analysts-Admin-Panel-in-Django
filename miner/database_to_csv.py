import sys, os.path
root_dir = os.path.dirname(os.path.dirname(__file__))
sys.path.append(root_dir)

import cli_app
import csv

from data.models import DataModel

cw_found = open("data/for_excel_data_found.csv", newline='')
cw_not_found = open("data/for_excel_data_not_found.csv", newline='')

csvwriter_found = csv.writer(cw_found)
csvwriter_not_found = csv.writer(cw_not_found)

all_found = DataModel.objects.filter(city_data_not_found=True).order_by("city")
all_not_found = DataModel.objects.filter(city_data_not_found=False).order_by("city")

csvwriter_not_found.writerow(["City", "Not Found"])
for d in all_not_found:
    row = [d.city, "No Data Found For This City"]
    csvwriter_not_found.writerow(row)
    cw_not_found.flush()

csvwriter_found.writerow(["City", "Name", "DBA", "Phone No", "Carrier Type", "Active Trucks", "Mailing Address",
                          "Effective Date", "TDLR"])
for d in all_found:
    row = [
        d.city,
        d.name,
        d.dba,
        d.phone,
        d.carrier_type,
        d.active_trucks,
        d.mailing_address,
        d.effective_date,
        d.active_no
    ]
    csvwriter_found.writerow(row)
    cw_found.flush()

cw_found.close()
cw_not_found.close()
