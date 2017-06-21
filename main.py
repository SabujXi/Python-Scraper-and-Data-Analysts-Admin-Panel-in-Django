import requests
import re
import csv

csvfile = open('data.csv', 'w', newline='')
csvwriter = csv.writer(csvfile)
csvwriter.writerow(["city", "name", "dba", "phone", "carrier_type", "active_trucks", "mailing_address", "effective_date", "active_no"])

# cities = ["ALLEN"]
cities = []
with open("cities.txt", "r", encoding="utf-8") as cf:
    txt = cf.read()
    l = txt.split("\n")
    for x in l:
        x = x.strip()
        if x:
            cities.append(x)

# TODO: Active no should be tuned so that it only shows active when it is active

customer_url_pattern = re.compile(r'<a href=(mccs_display\.asp\?mcrnumber=[0-9a-zA-Z]+)>', re.IGNORECASE | re.DOTALL)

company_name_pattern = re.compile(r'<TD.+?<strong>Name:.+?</strong>(.+?)</TD>', re.IGNORECASE | re.DOTALL)
dba_pattern = re.compile(r'<TD .+? align=left><strong>DBA:.+?</strong>(.+?)</TD>', re.IGNORECASE | re.DOTALL)
phone_pattern = re.compile(r'<td><strong>Phone:</strong>.+?([()0-9- ]+?)<BR><BR></td>', re.IGNORECASE | re.DOTALL)
carrier_type_pattern = re.compile(r'<td nowrap="nowrap"><strong>Carrier Type:</strong>&nbsp;&nbsp;(.+?)<br />', re.IGNORECASE | re.DOTALL)
active_trucks_pattern = re.compile(r'<b>Number of Active Tow Trucks:</b>.+?([0-9]+?)', re.IGNORECASE | re.DOTALL)
mailing_address_pattern = re.compile('<strong>Mailing:</strong><BR>(.+?)<strong>Physical:', re.IGNORECASE | re.DOTALL)
active_pattern = re.compile(r'<td nowrap="nowrap"><strong>Number:&nbsp;&nbsp;</strong>.+?([0-9a-zA-Z]+?)</b>', re.IGNORECASE | re.DOTALL)

date_pattern = re.compile(r'[0-9]{1,2}/[0-9]{1,2}/[0-9]{4}', re.IGNORECASE | re.DOTALL)


start_url = "https://www.tdlr.texas.gov/tools_search/mccs_search.asp"
search_city_form_url = "https://www.tdlr.texas.gov/tools_search/mccs_search_process.asp"
last_page_url = "https://www.tdlr.texas.gov/tools_search/mccs_information_display.asp"


session = requests.Session()

def get_effective_date(text):
    """
    <TD height="20" borderColor=gray align="center" width=10%><font size=1>6/7/2017</font></TD>

    :param text: 
    :return: 
    """
    date = date_pattern.findall(text)
    if len(date) >= 2:
        return date[1]
    else:
        print("****** Effective date not found ****")
        return ""


def get_page_number_urls(text: str):
    """
    Page Number<br>.*?
    <HR>

    :return: 
    """

    page_number_text_pat = re.compile("Page Number<br>.+?<HR>", re.IGNORECASE | re.DOTALL)
    page_nos_texts = page_number_text_pat.findall(text)
    if page_nos_texts:
        # print(page_nos_texts)
        page_no_text = page_nos_texts[0]
        url_pat = re.compile(r'<a href="(.+?)">', re.IGNORECASE | re.DOTALL)
        urls = url_pat.findall(page_no_text)
        return set(urls) if urls else None

    return None

class CitySearchDict:
    req_dict = {
        "searchtype": "city",
        "citydata": "ALVIN",
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


def process_customer_data(customer_res, full_url, city):
    restart = False
    print("\n")
    print("--------------------- customer data ----------------")
    print("url: ", full_url)
    print("current url: ", customer_res.url)
    dba = dba_pattern.findall(customer_res.text)
    if not dba:
        dba = "NO DATA"
    else:
        dba = dba[0].strip()
    print("DBA: ", dba)
    name = company_name_pattern.findall(customer_res.text)
    if name:
        name = name[0].strip()
    else:
        name = ""
    print("Name: ", name)
    phone = phone_pattern.findall(customer_res.text)
    if phone:
        phone = phone[0].strip()
    else:
        phone = ""
    print("Phone: ", phone)
    carrier_type = carrier_type_pattern.findall(customer_res.text)
    if carrier_type:
        carrier_type = carrier_type[0].strip()
    else:
        carrier_type = ""
    print("Carrier Type: ", carrier_type)
    active_trucks = active_trucks_pattern.findall(customer_res.text)
    if active_trucks:
        active_trucks = active_trucks[0].strip()
    else:
        active_trucks = ""
    print("Active Trucks: ", active_trucks)
    mailing_address = mailing_address_pattern.findall(customer_res.text)
    if mailing_address:
        mailing_address = mailing_address[0].strip()
        mailing_address = mailing_address.strip("<BR>")
        mailing_address = mailing_address.replace("<BR>", "")
        mailing_address = mailing_address.replace("&nbsp;", " ")
        l = mailing_address.split("\n")
        l2 = []
        for x in l:
            x2 = x.strip()
            l2.append(x2)
        mailing_address = "\r\n".join(l2)
    else:
        mailing_address = ""
    print("Mailing address: ", mailing_address)
    active_no = active_pattern.findall(customer_res.text)
    if active_no:
        active_no = active_no[0].strip()
    else:
        active_no = ""
    print("Active Number: ", active_no)

    last_resp = session.post(last_page_url, data={"infotype": "Insurance", "proc": ""}, headers={'referer': full_url})

    effective_date = get_effective_date(last_resp.text)
    print("Effective date: ", effective_date)

    data_array = [city, name, dba, phone, carrier_type, active_trucks, mailing_address, effective_date, active_no]
    csvwriter.writerow(data_array)
    csvfile.flush()

    print("\n\n")

    return restart


def process_customer_urls(customer_urls, city):
    restart = False
    # i = 0
    for url in customer_urls:
        # i += 1
        full_url = "https://www.tdlr.texas.gov/tools_search/" + url

        # for protecting from start url
        _r = session.get(start_url)
        customer_res = session.get(full_url)
        if customer_res.url.lower().strip() == start_url.lower().strip():
            restart = True

        # print(customer_res.text)
        # print(i, " --"*5)
        process_customer_data(customer_res, full_url, city)

    return restart




city_idx = 0


while city_idx < len(cities):
    # for city in cities:
    response0 = session.get(start_url)
    city = cities[city_idx]
    print("\n\n\n")
    print("City: ", city)
    print("------------------")

    response = session.post(search_city_form_url, data=CitySearchDict(city).get_data())


    print("History: ", response.history)

    # if result is found directly
    print("Response url: ", response.url)
    if response.url.startswith("https://www.tdlr.texas.gov/tools_search/mccs_display.asp?mcrnumber="):
                               # "https://www.tdlr.texas.gov/tools_search/mccs_display.asp?mcrnumber="
        print("Got direct result")
        process_customer_data(response, response.url, city)
        # process_customer_urls(customer_urls, city)
        city_idx += 1
        continue

    customer_urls = customer_url_pattern.findall(response.text)
    # print("More pages: ", get_page_number_urls(response.text))
    more_urls = get_page_number_urls(response.text)

    print("No of customer urls: ", len(customer_urls))

    if more_urls:
        for m_url in more_urls:
            m_url = m_url.replace("\n", "")
            m_url = m_url.replace("\r", "")
            m_url = m_url.replace("\t", "")
            # print("M Url: ", m_url)
            m_url = "https://www.tdlr.texas.gov/tools_search/" + m_url
            m_resp = session.get(m_url)
            customer_urls += customer_url_pattern.findall(m_resp.text)

    customer_urls = set(customer_urls)
    print("Final no of customer urls: ", len(customer_urls))

    if not customer_urls:
        csvwriter.writerow([city, "*** City Data Not Found ***"])
        city_idx += 1
        continue

    #####################
    process_customer_urls(customer_urls, city)

    city_idx += 1

csvfile.close()
