import requests
from tinydb import TinyDB, Query


CLIENT_SECRET = "MDJEMkQ5QTgtQUEwRC00QTRDLThDMDgtQTRGNEYyNjQ4NTEyOjUxNEQ4MTU5LTE5QzQtNENFOS05ODExLTE1QjVGNUYzRDEwMw=="
USERNAME = "ReedTransportraws"
PS = "QrE5cP?@YpsE"

db = TinyDB("db.json")
User = Query()
current_refresh_token = db.all()[0].get('refresh_token')
current_access_token = db.all()[0].get('access_token')


class initial_refresh_token:
    def __init__(self, CLIENT_SECRET, USERNAME, PS):
        self.CLIENT_SECRET = CLIENT_SECRET
        self.USERNAME = USERNAME
        self.PS = PS

    def get_initial_refresh_token(self):
        headers = {"Authorization": f"Basic {self.CLIENT_SECRET}",
                   "Content-Type": "application/x-www-form-urlencoded"}
        data = {"scope": "rates", "grant_type": "password",
                "username": self.USERNAME, "password": self.PS}
        r = requests.post("https://api-int.truckstop.com/auth/token",
                          headers=headers, data=data)

        json_response = r.json()
        return json_response['refresh_token']


class refresh_token(initial_refresh_token):
    def __init__(self, current_refresh_token, CLIENT_SECRET, USERNAME, PS):
        self.current_refresh_token = current_refresh_token
        initial_refresh_token.__init__(self, CLIENT_SECRET, USERNAME, PS)

    def get_refresh_token(self):
        if self.current_refresh_token == "":
            new_refresh_token = initial_refresh_token.get_initial_refresh_token(
                self)
            db.update({"refresh_token": new_refresh_token},
                      User.refresh_token == "")
            return new_refresh_token

        else:
            headers = {"Authorization": f"Basic {CLIENT_SECRET}",
                       "Content-Type": "application/x-www-form-urlencoded"}
            data = {"scope": "rates", "grant_type": "refresh_token",
                    "refresh_token": current_refresh_token}
            r = requests.post("https://api-int.truckstop.com/auth/token",
                              headers=headers, data=data)

            json_response = r.json()
            new_refresh_token = json_response['refresh_token']
            db.update({"refresh_token": new_refresh_token})
            return new_refresh_token


class access_token(refresh_token):
    def __init__(self, current_access_token, current_refresh_token, CLIENT_SECRET, USERNAME, PS):
        self.current_access_token = current_access_token
        refresh_token.__init__(self, current_refresh_token,
                               CLIENT_SECRET, USERNAME, PS)

    def get_access_token(self):
        headers = {"Authorization": f"Basic {CLIENT_SECRET}",
                   "Content-Type": "application/x-www-form-urlencoded"}
        data = {"scope": "rates", "grant_type": "refresh_token",
                "refresh_token": current_refresh_token}
        r = requests.post("https://api-int.truckstop.com/auth/token",
                          headers=headers, data=data)

        json_response = r.json()
        new_access_token = json_response['access_token']
        db.update({"access_token": new_access_token})
        return new_access_token

    def access_token_expired(self):
        headers = {"Authorization": f"Bearer {current_refresh_token}",
                   "Content-Type": "application/json"}
        r = requests.get(
            "https://api-int.truckstop.com/rates/v1/formulas", headers=headers)
        # json_response = r.json()
        return r.status_code


class view_config:
    def formulas(self):
        # if current_access_token == "":

        headers = {"Authorization": f"Bearer {current_refresh_token}",
                   "Content-Type": "application/json"}
        r = requests.get("https://api-int.truckstop.com/rates/v1/formulas",
                         headers=headers)
        json_response = r.json()
        return json_response


def main():
    # classes
    receive_refresh_token = refresh_token(
        current_refresh_token, CLIENT_SECRET, USERNAME, PS)

    receive_refresh_token.get_refresh_token()

    accesstoken = access_token(current_access_token,
                               current_refresh_token, CLIENT_SECRET, USERNAME, PS)

    print(accesstoken.access_token_expired())

    # view_formulas = view_config()
    # print(view_formulas.formulas())


if __name__ == "__main__":
    main()
