import re
from .patterns import (
    date_pattern,
    customer_url_pattern
)


def get_customer_page_urls(soup, add_to: set):
    customer_url_pattern = re.compile(r'^(mccs_display\.asp\?mcrnumber=)|(https://www\.tdlr\.texas\.gov/tools_search/mccs_display\.asp\?mcrnumber=)',
                                      re.IGNORECASE | re.DOTALL)
    urls = soup.find_all('a')
    for url_ in urls:
        url = url_.get("href")
        url = url.strip()
        url = url.replace("\t", "")
        url = url.replace("\r", "")
        url = url.replace("\n", "")
        if url:
            if url.startswith("mccs_display.asp?mcrnumber=") or \
               url.startswith("https://www.tdlr.texas.gov/tools_search/mccs_display.asp?mcrnumber="):
                add_to.add(url)


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


def prepare_session(referer, session):
    session.headers.update({'referer': referer})


def process_customer_page(source):
    pass


def get_city_data(city):
    pass


def clean_mailing_address(mailing_address):
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
    mailing_address = mailing_address.strip()

    return mailing_address


def print_data():
    pass


def process_more_url_links(more_urls, session, customer_urls):
    """
    For paginated urls
    :return: 
    """
    if more_urls:
        for m_url in more_urls:
            m_url = m_url.replace("\n", "")
            m_url = m_url.replace("\r", "")
            m_url = m_url.replace("\t", "")
            # print("M Url: ", m_url)
            m_url = "https://www.tdlr.texas.gov/tools_search/" + m_url
            m_resp = session.get(m_url)
            customer_urls += customer_url_pattern.findall(m_resp.text)

    return customer_urls

