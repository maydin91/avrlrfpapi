from flask import Flask, request, make_response
import truckstop_integration
import ujson
from flask_httpauth import HTTPBasicAuth
from tinydb import TinyDB, Query


app = Flask(__name__)
auth = HTTPBasicAuth()

db_access = TinyDB("db_access.json")
User = Query()
credentials = db_access.all()[0]


@auth.verify_password
def verify(username, password):
    if not(username and password):
        return False
    return credentials.get(username) == password


@app.route('/rate_lookup', methods=['GET', 'OPTIONS'])
@auth.login_required
def rate_lookup_handler():
    if request.method == 'OPTIONS':

        response = make_response()
        response.headers.add('Access-Control-Allow-Origin', '*')
        response.headers.add('Access-Control-Allow-Headers', '*')
        response.headers.add('Access-Control-Allow-Methods', '*')
        return response
    elif request.method == 'GET':
        params = request.get_json()
        resp_obj = truckstop_integration.rate_lookup("R", params['equipment_group'], "TL", None, None, None, params['orig_city'], params['orig_state'], None, None, params['dest_city'],
                                                     params['dest_state'], None, None, None, "Flat", "1 Year Avg Rates", params['fromDate'], params['toDate'])
        resp = resp_obj.process()
        r = make_response(ujson.dumps(resp), 200, {
                          'Content-type': 'application/JSON', 'Access-Control-Allow-Origin': '*'})
        return r


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, use_reloader=False)
