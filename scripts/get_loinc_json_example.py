import requests
from requests.exceptions import RequestException

#######################################################
#
# run loinc_json_flask.py to start server
#
#######################################################

resp = requests.get( 'http://127.0.0.1:5000/loinc/17811-1' )
if resp.status_code != 200:
    # Something went wrong.
    raise RequestException( resp.status_code )

print( resp.json() )


#######################################################
#######################################################
