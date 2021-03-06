import requests
from requests.exceptions import RequestException

#######################################################
#
# run loinc_json_flask.py to start server
#
#######################################################

resp = requests.get( 'https://loinc-part-search-demo.herokuapp.com/loinc/parts/descendants/LP56928-2' )
if resp.status_code != 200:
    # Something went wrong.
    raise RequestException( resp.status_code )

print( resp.json() )


#######################################################
#######################################################
