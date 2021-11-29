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
            db.update({"refresh_token": new_refresh_token})
            self.current_refresh_token = db.all()[0].get('refresh_token')
            return new_refresh_token

        else:
            headers = {"Authorization": f"Basic {CLIENT_SECRET}",
                       "Content-Type": "application/x-www-form-urlencoded"}
            data = {"scope": "rates", "grant_type": "refresh_token",
                    "refresh_token": self.current_refresh_token}
            r = requests.post("https://api-int.truckstop.com/auth/token",
                              headers=headers, data=data)

            json_response = r.json()
            new_refresh_token = json_response['refresh_token']
            db.update({"refresh_token": new_refresh_token})
            self.current_refresh_token = new_refresh_token
            return new_refresh_token




class access_token(refresh_token):
    def __init__(self, current_access_token, current_refresh_token, CLIENT_SECRET, USERNAME, PS):
        self.current_access_token = current_access_token
        refresh_token.__init__(self, current_refresh_token,
                               CLIENT_SECRET, USERNAME, PS)

    def access_token_expired(self):
        headers = {"Authorization": f"Bearer {self.current_access_token}",
                   "Content-Type": "application/json"}
        r = requests.get(
            "https://api-int.truckstop.com/rates/v1/formulas", headers=headers)
        return r.status_code

    def get_access_token(self):
        if self.access_token_expired() != 200:
            refresh_token.get_refresh_token(self)

            headers = {"Authorization": f"Basic {CLIENT_SECRET}",
                       "Content-Type": "application/x-www-form-urlencoded"}
            data = {"scope": "rates", "grant_type": "refresh_token",
                    "refresh_token": self.current_refresh_token}
            r = requests.post("https://api-int.truckstop.com/auth/token",
                              headers=headers, data=data)
            json_response = r.json()
            new_access_token = json_response['access_token']
            new_refresh_token = json_response['refresh_token']
            db.update({"access_token": new_access_token})
            db.update({"refresh_token": new_refresh_token})
            self.current_refresh_token = db.all()[0].get('refresh_token')
            self.current_access_token = db.all()[0].get('access_token')
            return new_access_token
        else:
            return current_access_token


class view_config(access_token):
    def __init__(self, current_access_token, current_refresh_token, CLIENT_SECRET, USERNAME, PS):

        access_token.__init__(self, current_access_token, current_refresh_token,
                           CLIENT_SECRET, USERNAME, PS)
    def formulas(self):
        headers = {"Authorization": f"Bearer {self.current_access_token}",
                   "Content-Type": "application/json"}
        r = requests.get("https://api-int.truckstop.com/rates/v1/formulas",
                         headers=headers)
        json_response = r.json()
        return json_response


    def formula_process(self):
        if access_token.access_token_expired(self) == 200:
            return self.formulas()
        else:
            access_token.get_refresh_token(self)
            access_token.get_access_token(self)
            return self.formulas()

    def sources(self):
        headers = {"Authorization": f"Bearer {self.current_access_token}",
                   "Content-Type": "application/x-www-form-urlencoded"}
        r = requests.get("https://api-int.truckstop.com/rates/v1/sources",
                         headers=headers)
        json_response = r.json()
        return json_response

    def source_process(self):
        if access_token.access_token_expired(self) == 200:
            return self.sources()
        else:
            access_token.get_refresh_token(self)
            access_token.get_access_token(self)
            return self.sources()

    def rate_analysis_credtis(self):
        headers = {"Authorization": f"Bearer {self.current_access_token}",
                   "Content-Type": "application/json"}
        r = requests.get("https://api-int.truckstop.com/rates/v1/account/billing",
                         headers=headers)
        json_response = r.json()
        return json_response

    def rate_analysis_credits_process(self):
        if access_token.access_token_expired(self) == 200:
            return self.rate_analysis_credtis()
        else:
            access_token.get_refresh_token(self)
            access_token.get_access_token(self)
            return self.rate_analysis_credtis()


def main():
    # classes

    # receive_refresh_token = refresh_token(
    #     current_refresh_token, CLIENT_SECRET, USERNAME, PS)

    # print(receive_refresh_token.access_token_expired())

    # receive_access_token = access_token(
    #     current_access_token, current_refresh_token, CLIENT_SECRET, USERNAME, PS)

    # print(receive_access_token.access_token_expired())

    receive_formula = view_config(current_access_token, current_refresh_token, CLIENT_SECRET, USERNAME, PS)

    print(receive_formula.rate_analysis_credits_process())


if __name__ == "__main__":
    main()
