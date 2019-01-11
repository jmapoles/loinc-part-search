# --------------------------------------------------------------------------------------------
# --------------------------------------------------------------------------------------------


from loinc_part_search.db_data.access_loinc import AccessLOINC
from loinc_part_search.db_data.access_json import AccessJSON


# --------------------------------------------------------------------------------------------
# --------------------------------------------------------------------------------------------

access_loinc = AccessLOINC ( "mysql" , "localhost", "root", "JANN1qwe1!", "loinc_264" )
access_loinc.make_connection()

access = AccessJSON( access_loinc )


def get_object():

    test_obj = access_loinc.get_eav_obj_of_id ( 1200 )
    test_obj.display()
    print("\n\n\n")
    print( access.get_json_of_obj_id( 1200 ) )


def get_object_of_code():

    test_obj = access_loinc.get_eav_obj_of_code ( "11050-2" )
    test_obj.display()

def get_parent_objects():

    parents = access_loinc.get_parent_obj_of_id( 1200 )

    for parent in parents:

        parent.display()

def get_children_objects():

    children = access_loinc.get_child_obj_of_id( 97185 )

    for child in children:
        child.display(0)


def get_ancestor_objects():

    print( "")
    for ancestor in access_loinc.get_ancestors_obj_of_id( 1200 ):
        ancestor.display(0)

def get_ancestor_objects_to_level():

    print( " 1")
    for ancestor in access_loinc.get_ancestors_obj_of_id_to_level( 1200 , 1 ):
        ancestor.display(0)

    print( " 2 ")
    for ancestor in access_loinc.get_ancestors_obj_of_id_to_level( 1200 , 2 ):
        ancestor.display(0)

    print( " 3")
    for ancestor in access_loinc.get_ancestors_obj_of_id_to_level( 1200 , 3 ):
        ancestor.display(0)


def get_descendant_objects():

    for descendant in access_loinc.get_descendants_obj_of_id( 97176 ):
        descendant.display(0)

def get_descendant_map():

    map = access_loinc.get_descendants_obj_of_id_as_map( 97176 )
    map.display_as_hierarchy()


def get_json_descendants_of_loinc_code():

    print( access.get_json_descendant_of_loinc_part_code ( "41759-2" ) )


# --------------------------------------------------------------------------------------------

def main():

    print ( "\nGet object from code:" )
    get_object_of_code()

    print( "\nGet parent:")
    get_parent_objects()

    print( "\nGet children:")
    get_children_objects()

    # print( "\nGet ancestors:")
    # get_ancestor_objects()
    #
    # print( "\nGet ancestors to level:")
    # get_ancestor_objects_to_level()
    #
    # print( "\nGet descendants:")
    # get_descendant_objects()
    #
    # print( "\nGet descendants map:")
    # get_descendant_map()
    #
    # print( "\nGet descendants:")
    # get_json_descendants_of_loinc_code()


# --------------------------------------------------------------------------------------------
# --------------------------------------------------------------------------------------------


if __name__ == '__main__':
    main()

# --------------------------------------------------------------------------------------------
# --------------------------------------------------------------------------------------------
