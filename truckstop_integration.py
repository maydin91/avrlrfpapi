import requests


CLIENT_SECRET = "MDJEMkQ5QTgtQUEwRC00QTRDLThDMDgtQTRGNEYyNjQ4NTEyOjUxNEQ4MTU5LTE5QzQtNENFOS05ODExLTE1QjVGNUYzRDEwMw=="

USERNAME = "ReedTransportraws"
PS = "QrE5cP?@YpsE"


def get_initial_refresh_token(username, password, clientsecret):
    headers = {"Authorization": f"Basic {clientsecret}",
               "Content-Type": "application/x-www-form-urlencoded"}
    data = {"scope": "rates", "grant_type": "password",
            "username": username, "password": password}
    r = requests.post("https://api-int.truckstop.com/auth/token",
                      headers=headers, data=data)

    json_response = r.json()

    return json_response['refresh_token']


def get_refresh_token(current_refresh_token):
    headers = {"Authorization": f"Basic {clientsecret}",
               "Content-Type": "application/x-www-form-urlencoded"}
    data = {"scope": "rates", "grant_type": "refresh_token",
            "refresh_token": current_refresh_token}
    r = requests.post("https://api-int.truckstop.com/auth/token",
                      headers=headers, data=data)

    json_response = r.json()

    return json_response['refresh_token']


# Create a class tomorrow

# def get_access_token():
#     requests.post("https://api-int.truckstop.com/rates/v1/analysis")


# def lookup_lane():


print(get_initial_refresh_token(USERNAME, PS, CLIENT_SECRET))

print(get_refresh_token(USERNAME, PS, CLIENT_SECRET))

# headers = {"Authorization": "Bearer 0f6cb60d-f11a-4b12-9aef-c7d084c97d38","Content-Type": "application/json"}
# data = {"startDtTime":yesterdaystarttime, "endDtTime":yesterdayendtime, "pageNumber":pagenumber}
# r = requests.post('https://www.fleetview.net/restapi/events', headers=headers, json=data)
