import requests
from tinydb import TinyDB, Query
import json
import datetime
import psycopg2


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
        self.current_refresh_token = intial_refresh_token
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

            print(r.status_code)
            if r.status_code != 200:
                return initial_refresh_token.get_initial_refresh_token(self)
            else:
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


class rate_lookup(lanes):
    DB_HOST = "ec2-50-19-125-153.compute-1.amazonaws.com"
    DB_NAME = "d2ce1t4f7orbvr"
    DB_USER = "u9d8kvc6ea76ag"
    DB_PASS = "pfb7e47665fc06249a5ec338ab7ed3f7b3db879e72f907bbaffd05e523815613e"
    now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M')

    def insert_truckstop_integration(self, conn, query):
        cursor = conn.cursor()
        cursor.execute(query)

        conn.commit()
        cursor.close()
        conn.close()

    def generate_query(self, orig_city, orig_state, orig_zip, dest_city, dest_state, dest_zip, eq_group, rate_type, fromdate, todate, miles, flatrate, fuelcost, rpm, allin):
        query = f"insert into truckstop_data_store(lookupdate,orig_city, orig_state,orig_zip, dest_city, dest_state, dest_zip, eq_group, rate_type,fromdate,todate, miles, flatrate, fuelcost, rpm, allin) values('{now}','{orig_city}', '{orig_state}','{orig_zip}', '{dest_city}', '{dest_state}', '{dest_zip}', '{eq_group}', '{rate_type}','{fromdate}','{todate}', '{miles}', '{flatrate}', '{fuelcost}', '{rpm}', '{allin}')"
        return query

    def process(self):
        try:
            # get_rate = lanes(params['equipment_group'], "Flat", "TL", None, None, None, params['orig_city'], params['orig_state'], None, None, params['dest_city'],
                             # params['dest_state'], None, None, None, "Flat", "1 Year Avg Rates", params['fromDate'], params['toDate'])
            # get_rate = resp_obj
            result = lanes.lane_process(self)
            conn = psycopg2.connect(
                dbname=self.DB_NAME, user=self.DB_USER, password=self.DB_PASS, host=self.DB_HOST)

            query = self.generate_query(self.originCity, self.originState, result['originZip'],
                                        self.destinationCity, self.destinationState, result['destinationZip'], self.equipmentGroup, "Flat", self.timeFrameFromDate, self.timeFrameToDate, result['miles'], result['flatRate'], result['fuelCost'], result['rpm'], result['allin'])

            insert_truckstop_integration(self, conn, query)

            return result

        except Exception as e:
            print(e)
            return {'status': 'failed'}

            # def main():
            # classes

            # receive_refresh_token = initial_refresh_token()

            # print(receive_refresh_token.get_initial_refresh_token())

            # receive_access_token = access_token()

            # print(receive_access_token.get_access_token())

            # receive_formula = view_config()

            # print(receive_formula.formula_process())

            #     get_rate = lanes("R", "Flat", "TL", None, None, None, "Atlanta", "GA", None, None, "Orlando",
            #                      "FL", None, None, None, "Flat", "1 Year Avg Rates", "2021-01-01", "2021-11-30")

            #     print(get_rate.lane_process())

            # if __name__ == "__main__":
            #     main()
