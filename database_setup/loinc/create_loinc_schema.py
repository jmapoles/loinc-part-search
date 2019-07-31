from loinc_part_search.database_connection.db_connection import DBConnection


# --------------------------------------------------------
class CreatePostgresSchema(DBConnection):

    def __init__(self, type , server, user_name, password, database , schema ):

        self.db_conn = DBConnection( type , server, user_name, password, database)

        query = f" CREATE schema {schema} "
        self.db_conn.execute_query( query );

        query = f" CREATE TABLE {schema}.codes ( id int not null , defining_id int not null , " \
                f" defining_value varchar(1000) not null , primary key( id ) )  "
        self.db_conn.execute_query( query );

        query = f" CREATE TABLE {schema}.code_hierarchy (  parent_id int not null , id int not null )  "
        self.db_conn.execute_query( query );

        query = f" CREATE TABLE {schema}.code_attributes ( id int not null , " \
                f" attribute_id int not null , attribute_value varchar(1000) not null ,  preferred boolean )  "
        self.db_conn.execute_query( query );

        query = f" create index co_parent id_idx_id on {schema}.code_hierarchy( id ) "
        self.db_conn.execute_query( query );
        query = f" create index code_h_idx_parent id on {schema}.code_hierarchy( parent_id ) "
        self.db_conn.execute_query( query );
        query = f" create index code_att_id on {schema}.code_attributes( id ) "

        self.db_conn.close_connection()


    # --------------------------------------------------------
    # --------------------------------------------------------


# --------------------------------------------------------------------------------------------
# --------------------------------------------------------------------------------------------

def main():

    CreatePostgresSchema( "postgres" , "localhost" , "postgres" , "JANN1qwe1!" , "USMedicalCodes" , "loinc_265" )


# --------------------------------------------------------------------------------------------
# --------------------------------------------------------------------------------------------

if __name__ == '__main__':

    main()


# --------------------------------------------------------------------------------------------
# --------------------------------------------------------------------------------------------
