import requests
import html5lib
from bs4 import BeautifulSoup
from details import *

session = requests.Session()

url = "https://www.vitchennaievents.com/conf1/login/"

details = details()

payload={'username-login': details["username"],
'password-login': details["password"],
'login-form-button': ""}

initial = session.request("POST", url, data=payload)
cookies = session.cookies.get_dict()

url = "https://www.vitchennaievents.com/conf1/profile/"
response = session.request("GET", url, cookies=cookies)

soup = BeautifulSoup(response.text, 'html5lib')
getTable = soup.find("table", {"cellspacing": "7px", "style": "width: 100%"})
profile_data = [i.getText() for i in getTable.find_all("p", {"style": "font-size: 30px;  font-weight: 500;"})]

profile = {"RegNo": profile_data[0], "Name": profile_data[1], "Email": profile_data[2], "Phone": profile_data[3], "Institute": profile_data[4]}

events = []
getModal = soup.find_all("div", {"class": "modal-body"})
for i in getModal: 
    try:
        getModalTable = i.find("table", {"style": "width: 100%;"})
        data = getModalTable.find("td", {"id": "name", "rowspan": "2"})
        data = data.getText().strip().split(" ")
        
        eventExtra = getModalTable.find_all("td", {"id": "value"})
        info = [i.getText() for i in eventExtra]
        store = []
        for j in data:
            if len(j)!=0:
                store.append(j)
        name = " ".join(store[:store.index("Order")])
        eventId = store[store.index(":")+1]
        res = {"EventName": name, "EventId": eventId, "EventVenue": info[0], "EventDate": info[1], "EventTime": info[2]}
        events.append(res)
    except Exception as e:
        pass

profile["Events"] = events
print(profile)