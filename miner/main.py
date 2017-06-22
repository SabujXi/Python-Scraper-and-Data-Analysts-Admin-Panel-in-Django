import requests
import re
import csv
from .data_classes import (
    CitySearchDict,
    CustomerDataFromHTMLSource
)
# import bs4
# import cli_app
# from data.models import DataModel

from .patterns import (
    customer_url_pattern,
    date_pattern,
    active_pattern,
    mailing_address_pattern,
    carrier_type_pattern,
    phone_pattern,
    company_name_pattern,
    dba_pattern,
    active_trucks_pattern,
)

from .urls import (
    last_page_url,
    search_city_form_url,
    search_page_url
)

from .data.cities_array import (
    cities
)

from .functions import (
    get_effective_date,
    get_city_data,
    get_page_number_urls,
    get_customer_page_urls,
    prepare_session,
    process_customer_page,
    clean_mailing_address,
    process_more_url_links
)

from .run_config import (
    csv_file_name
)

session = requests.Session()
session.headers.update({'User-Agent': 'Mozilla/5.0'})

"""
Steps:
1) Get list of city
2) Get Customer list in the city
    |)  process next pages and accumulate the customer urls
3) Process the customer link
4) Get the effective date
"""


def scrape(cities, session):
    csvfile = open(csv_file_name, 'w', newline='')
    csvwriter = csv.writer(csvfile)
    csvwriter.writerow(
        ["city", "name", "dba", "phone", "carrier_type", "active_trucks", "mailing_address", "effective_date",
         "active_no"])
    city_idx = 0
    record_no = 1
    while city_idx < len(cities):
        city = cities[city_idx]
        print("City NO: %s \nCity Name: %s" % (city_idx+1, city))
        # for city in cities:
        response0 = session.get(search_page_url)
        print("\n\n\n");print("City: ", city);print("------------------")
        response = session.post(search_city_form_url, data=CitySearchDict(city).get_data())
        # print("History: ", response.history);
        print("Response url: ", response.url)
        if response.url.startswith("https://www.tdlr.texas.gov/tools_search/mccs_display.asp?mcrnumber="):
            print("Got direct result")
            customer_data = process_customer_data(response, response.url, city)
            customer_data.set_city_data_not_found(False)
            customer_data.save_to_csv(csvwriter, csvfile)
            print("Record NO: %s" % record_no)
            record_no += 1
            customer_data.print_data()
            # process_customer_urls(customer_urls, city)
            city_idx += 1
            continue

        customer_urlsF = customer_url_pattern.findall(response.text)
        # print("More pages: ", get_page_number_urls(response.text))
        more_urls = get_page_number_urls(response.text)
        print("No of customer urls: ", len(customer_urlsF))
        customer_urls_ = process_more_url_links(more_urls, session, customer_urlsF)
        # print("URLS NOW: ", customer_urls_)
        customer_urls_set = set()
        customer_urls = []
        for curl in customer_urls_:
            if curl in customer_urls_set:
                print("Duplicate URL")
            else:
                customer_urls.append(curl)
                customer_urls_set.add(curl)
        print("Final no of customer urls: ", len(customer_urls))

        if not customer_urls:
            customer_data = CustomerDataFromHTMLSource()
            customer_data.set_city_data_not_found(True)
            customer_data.set_city(city)
            customer_data.save_to_csv(csvwriter, csvfile)
            print("Record NO: %s" % record_no)
            record_no += 1
            customer_data.print_data()
            city_idx += 1
            continue

        #####################
        restart, data_list = process_customer_data_page_urls_and_data(customer_urls, city)
        if restart:
            print("Restart required due to session reset...\n" * 10)
            restart, data_list = process_customer_data_page_urls_and_data(customer_urls, city)

        for c_d in data_list:
            c_d.save_to_csv(csvwriter, csvfile)
            c_d.print_data()
            print("Record NO: %s" % record_no)
            record_no += 1
        city_idx += 1
    csvfile.close()


def process_customer_data(customer_res, full_url, city):
    cd = customer_data = CustomerDataFromHTMLSource()
    cd.set_city(city)
    print("\n")
    print("--------------------- customer data ----------------")
    print("url: ", full_url)
    print("current url: ", customer_res.url)
    dba = dba_pattern.findall(customer_res.text)
    cd.set_dba(dba)

    name = company_name_pattern.findall(customer_res.text)
    cd.set_name(name)

    phone = phone_pattern.findall(customer_res.text)
    cd.set_phone(phone)

    carrier_type = carrier_type_pattern.findall(customer_res.text)
    cd.set_carrier_type(carrier_type)

    active_trucks = active_trucks_pattern.findall(customer_res.text)
    cd.set_active_trucks(active_trucks)

    mailing_address = mailing_address_pattern.findall(customer_res.text)
    cd.set_mailing_address(mailing_address)

    active_no = active_pattern.findall(customer_res.text)
    cd.set_active_no(active_no)

    last_resp = session.post(last_page_url, data={"infotype": "Insurance", "proc": ""}, headers={'referer': full_url})

    effective_date = get_effective_date(last_resp.text)
    cd.set_effective_date(effective_date)

    return customer_data
    # return restart


def process_customer_data_page_urls_and_data(customer_urls, city):
    data_list = []
    restart = False
    # i = 0
    for url in customer_urls:
        # i += 1
        full_url = "https://www.tdlr.texas.gov/tools_search/" + url
        # for protecting from start url
        # _r = session.get(search_page_url)
        customer_res = session.get(full_url)
        if customer_res.url.lower().strip() == search_page_url.lower().strip():
            restart = True
        customer_data = process_customer_data(customer_res, full_url, city)
        data_list.append(customer_data)
    return restart, data_list



