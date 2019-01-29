from flask import Flask , render_template
import loinc_part_search.db_data as conn


app = Flask( __name__ )

# heroku
access_loinc = conn.AccessLOINC( "postgres" , \
                                 "ec2-54-225-227-125.compute-1.amazonaws.com", \
                                 "qcdvginxdwqnou", \
                                 "0c065f21b52d1826a3beea594c4f78d4f3bf62ef98824dfe1687b29ffb56c18c", \
                                 "dfh8skpjeee9sf" )

access_loinc.make_connection()

access = conn.AccessJSON( access_loinc )


@app.route( '/' )
def index():
    return render_template( "index.html" )


@app.route( '/loinc/<code>' )
def loinc( code ):
    print( "" )
    return access.get_json_of_loinc_code( code )


@app.route( '/loinc/siblings/<code>' )
def loinc_siblings( code ):
    return access.get_json_siblings_of_loinc_code( code )


@app.route( '/loinc/cousins/<code>' )
def loinc_cousins( code ):
    return access.get_json_cousins_of_loinc_code( code )


@app.route( '/loinc/parents/<code>' )
def loinc_parents( code ):
    return access.get_json_parents_of_loinc_code( code )


@app.route( '/loinc/parts/<code>' )
def loinc_part( code ):
    return access.get_json_of_loinc_part_code( code )


@app.route( '/loinc/parts/descendants/<code>' )
def loinc_part_descendants( code ):
    return access.get_json_descendant_of_loinc_part_code( code )


@app.route( '/loinc/parts/parents/<code>' )
def loinc_part_parents( code ):
    return access.get_json_parents_of_loinc_part_code( code )


if __name__ == '__main__':

    app.run( )
