import re

customer_url_pattern = re.compile(r'<a href=(mccs_display\.asp\?mcrnumber=[0-9a-zA-Z]+)>', re.IGNORECASE | re.DOTALL)
company_name_pattern = re.compile(r'<TD.+?<strong>Name:.+?</strong>(.+?)</TD>', re.IGNORECASE | re.DOTALL)
dba_pattern = re.compile(r'<TD .+? align=left><strong>DBA:.+?</strong>(.+?)</TD>', re.IGNORECASE | re.DOTALL)
phone_pattern = re.compile(r'<td><strong>Phone:</strong>.+?([()0-9- ]+?)<BR><BR></td>', re.IGNORECASE | re.DOTALL)
carrier_type_pattern = re.compile(r'<td nowrap="nowrap"><strong>Carrier Type:</strong>&nbsp;&nbsp;(.+?)<br />', re.IGNORECASE | re.DOTALL)
active_trucks_pattern = re.compile(r'<b>Number of Active Tow Trucks:</b>.+?([0-9]+).+?<BR>', re.IGNORECASE | re.DOTALL)
mailing_address_pattern = re.compile('<strong>Mailing:</strong><BR>(.+?)<strong>Physical:', re.IGNORECASE | re.DOTALL)
active_pattern = re.compile(r'<td nowrap="nowrap"><strong>Number:&nbsp;&nbsp;</strong>.+?([0-9a-zA-Z]+?)</b>', re.IGNORECASE | re.DOTALL)

date_pattern = re.compile(r'[0-9]{1,2}/[0-9]{1,2}/[0-9]{4}', re.IGNORECASE | re.DOTALL)