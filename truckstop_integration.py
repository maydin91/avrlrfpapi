import requests
from tinydb import TinyDB, Query
import json
import pyodbc


class initial_refresh_token:

    CLIENT_SECRET = "MDJEMkQ5QTgtQUEwRC00QTRDLThDMDgtQTRGNEYyNjQ4NTEyOjUxNEQ4MTU5LTE5QzQtNENFOS05ODExLTE1QjVGNUYzRDEwMw=="
    USERNAME = "ReedTransportraws"
    PS = "QrE5cP?@YpsE"
    db = TinyDB("db.json")
    current_refresh_token = db.all()[0].get('refresh_token')
    current_access_token = db.all()[0].get('access_token')

    def get_initial_refresh_token(self):
        headers = {"Authorization": f"Basic {self.CLIENT_SECRET}",
                   "Content-Type": "application/x-www-form-urlencoded"}
        data = {"scope": "rates", "grant_type": "password",
                "username": self.USERNAME, "password": self.PS}
        r = requests.post("https://api-int.truckstop.com/auth/token",
                          headers=headers, data=data)

        json_response = r.json()
        intial_refresh_token = json_response['refresh_token']
        self.db.update({"refresh_token": intial_refresh_token})
        return intial_refresh_token


class refresh_token(initial_refresh_token):

    def get_refresh_token(self):
        if self.current_refresh_token == "":
            new_refresh_token = initial_refresh_token.get_initial_refresh_token(
                self)
            self.db.update({"refresh_token": new_refresh_token})
            self.current_refresh_token = self.db.all()[0].get('refresh_token')
            return new_refresh_token

        else:
            headers = {"Authorization": f"Basic {self.CLIENT_SECRET}",
                       "Content-Type": "application/x-www-form-urlencoded"}
            data = {"scope": "rates", "grant_type": "refresh_token",
                    "refresh_token": self.current_refresh_token}
            r = requests.post("https://api-int.truckstop.com/auth/token",
                              headers=headers, data=data)

            json_response = r.json()
            new_refresh_token = json_response['refresh_token']
            self.db.update({"refresh_token": new_refresh_token})
            self.current_refresh_token = new_refresh_token
            return new_refresh_token


class access_token(refresh_token):

    def access_token_expired(self):
        headers = {"Authorization": f"Bearer {self.current_access_token}",
                   "Content-Type": "application/json"}
        r = requests.get(
            "https://api-int.truckstop.com/rates/v1/formulas", headers=headers)
        return r.status_code

    def get_access_token(self):
        if self.access_token_expired() != 200:
            refresh_token.get_refresh_token(self)

            headers = {"Authorization": f"Basic {self.CLIENT_SECRET}",
                       "Content-Type": "application/x-www-form-urlencoded"}
            data = {"scope": "rates", "grant_type": "refresh_token",
                    "refresh_token": self.current_refresh_token}
            r = requests.post("https://api-int.truckstop.com/auth/token",
                              headers=headers, data=data)
            json_response = r.json()
            new_access_token = json_response['access_token']
            new_refresh_token = json_response['refresh_token']
            self.db.update({"access_token": new_access_token})
            self.db.update({"refresh_token": new_refresh_token})
            self.current_refresh_token = self.db.all()[0].get('refresh_token')
            self.current_access_token = self.db.all()[0].get('access_token')
            return new_access_token
        else:
            return current_access_token


class view_config(access_token):

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


class lanes(access_token):
    def __init__(self, typeOfEquipments, equipmentGroup, mode, laneNumber, targetRate, miles, originCity, originState, originCountry, originZip, destinationCity, destinationState, destinationCountry, destinationZip, commodityName, rateType, calculatedRateFormula, timeFrameFromDate, timeFrameToDate):
        self.typeOfEquipments = typeOfEquipments
        self.equipmentGroup = equipmentGroup
        self.mode = mode
        self.laneNumber = laneNumber
        self.targetRate = targetRate
        self.miles = miles
        self.originCity = originCity
        self.originState = originState
        self.originCountry = originCountry
        self.originZip = originZip
        self.destinationCity = destinationCity
        self.destinationState = destinationState
        self.destinationCountry = destinationCountry
        self.destinationZip = destinationZip
        self.commodityName = commodityName
        self.rateType = rateType
        self.calculatedRateFormula = calculatedRateFormula
        self.timeFrameFromDate = timeFrameFromDate
        self.timeFrameToDate = timeFrameToDate

    def create_json_body(self):
        body = {
            "lane": [
                {
                    "typeOfEquipments": self.typeOfEquipments,
                    "equipmentGroup": self.equipmentGroup,
                    "mode": self.mode,
                    "laneNumber": self.laneNumber,
                    "targetRate": self.targetRate,
                    "miles": self.miles,
                    "originCity": self.originCity,
                    "originState": self.originState,
                    "originCountry": self.originCountry,
                    "originZip": self.originZip,
                    "destinationCity": self.destinationCity,
                    "destinationState": self.destinationState,
                    "destinationCountry": self.destinationCountry,
                    "destinationZip": self.destinationZip,
                    "commodityName": self.commodityName,
                    "rateType": self.rateType
                }
            ],
            "calculatedRateFormula": self.calculatedRateFormula,
            "timeFrameFromDate": self.timeFrameFromDate,
            "timeFrameToDate": self.timeFrameToDate
        }
        json_body = json.dumps(body)
        return json_body

    def lane_lookup(self):
        headers = {"Authorization": f"Bearer {self.current_access_token}",
                   "Content-Type": "application/json"}
        data = self.create_json_body()
        r = requests.post("https://api-int.truckstop.com/rates/v1/analysis",
                          headers=headers, data=data)
        json_response = r.json()
        return json_response

    def lane_process(self):
        if access_token.access_token_expired(self) == 200:
            return self.lane_lookup()
        else:
            access_token.get_refresh_token(self)
            access_token.get_access_token(self)
            return self.lane_lookup()


class insert_db(lanes):
    conn = pyodbc.connect(

        "Driver={SQL Server Native Client 11.0};"
        "Server=RT-TABDB;"
        "Database=McLeodTMS;"
        "Trusted_Connection=no;"
        "UID=SuperUser;"
        "PWD=Sm00thy!!@RTS;"
    )

    now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M')

    def insert_truckstop_integration(self, query):

    cursor = conn.cursor()
    cursor.execute(query)

    conn.commit()
    cursor.close()
    conn.close()

    def generate_query(self):
        query = f"insert into truckstop_data_store values('{self.now}','{}',)"
        return query


def main():
    # classes

    # receive_refresh_token = initial_refresh_token()

    # print(receive_refresh_token.get_initial_refresh_token())

    # receive_access_token = access_token()

    # print(receive_access_token.get_access_token())

    # receive_formula = view_config()

    # print(receive_formula.formula_process())

    # get_rate = lanes("R", "Flat", "TL", null, null, null, "Ballinger", "TX", null, null, "Tampa",
    #                  "FL", null, null, null, "Flat", "1 Year Avg Rates", "2021-11-01", "2021-11-10")

    get_rate = lanes("R", "Flat", "TL", None, None, None, "Ballinger", "TX", None, None, "McDonough",
                     "GA", None, None, None, "Flat", "1 Year Avg Rates", "2021-11-01", "2021-11-10")

    print(get_rate.lane_process())


if __name__ == "__main__":
    main()
