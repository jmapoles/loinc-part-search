# --------------------------------------------------------

from loinc_part_search.loinc_objects.eav_objects import EAVObject , EAVMap

# --------------------------------------------------------


class TestConstants:
    """
    Constants used in testing

    model of objects

                                        part: 1000, LP-1000

                            part: 1001, LP-1001      part: 1002, LP-1002

                part: 1003, LP-1003     part: 1004, LP-1004     part: 1005, LP-1005

                code: 1006, L-1006      code: 1007, L-1007      code: 1008, L-1008
                code: 1009, L-1009      code: 1010, L-1010      code: 1011, L-1011

    """

    # map test
    eav_map = EAVMap()

    obj_id_1000 = 1000
    obj_id_1001 = 1001
    obj_id_1002 = 1002
    obj_id_1003 = 1003
    obj_id_1004 = 1004
    obj_id_1005 = 1005
    obj_id_1006 = 1006
    obj_id_1007 = 1007
    obj_id_1008 = 1008
    obj_id_1009 = 1009
    obj_id_1010 = 1010
    obj_id_1011 = 1011

    part_1000  = EAVObject ( 1000 , 'LOINC Part Code' , '1000' , 'Name' , 'LP-1000' )
    part_1001  = EAVObject ( 1001 , 'LOINC Part Code' , '1001' , 'Name' , 'LP-1001' )
    part_1002  = EAVObject ( 1002 , 'LOINC Part Code' , '1002' , 'Name' , 'LP-1002' )
    part_1003  = EAVObject ( 1003 , 'LOINC Part Code' , '1003' , 'Name' , 'LP-1003' )
    part_1004  = EAVObject ( 1004 , 'LOINC Part Code' , '1004' , 'Name' , 'LP-1004' )
    part_1005  = EAVObject ( 1005 , 'LOINC Part Code' , '1005' , 'Name' , 'LP-1005' )
    code_1006  = EAVObject ( 1006 , 'LOINC Code' , '1006' , 'Name' , 'L-1006' )
    code_1007  = EAVObject ( 1007 , 'LOINC Code' , '1007' , 'Name' , 'L-1007' )
    code_1008  = EAVObject ( 1008 , 'LOINC Code' , '1008' , 'Name' , 'L-1008' )
    code_1009  = EAVObject ( 1009 , 'LOINC Code' , '1009' , 'Name' , 'L-1009' )
    code_1010  = EAVObject ( 1010 , 'LOINC Code' , '1010' , 'Name' , 'L-1010' )
    code_1011  = EAVObject ( 1011 , 'LOINC Code' , '1011' , 'Name' , 'L-1011' )

    name_1000 = 'LOINC Part Code: 1000, LP-1000'
    name_1001 = 'LOINC Part Code: 1001, LP-1001'
    name_1002 = 'LOINC Part Code: 1002, LP-1002'
    name_1003 = 'LOINC Part Code: 1003, LP-1003'
    name_1004 = 'LOINC Part Code: 1004, LP-1004'
    name_1005 = 'LOINC Part Code: 1005, LP-1005'
    name_1006 = 'LOINC Code: 1006, L-1006'
    name_1007 = 'LOINC Code: 1007, L-1007'
    name_1008 = 'LOINC Code: 1008, L-1008'
    name_1009 = 'LOINC Code: 1009, L-1009'
    name_1010 = 'LOINC Code: 1010, L-1010'
    name_1011 = 'LOINC Code: 1011, L-1011'


    eav_map.add ( 1000 , part_1000 )
    eav_map.add ( 1001 , part_1001 )
    eav_map.add ( 1002 , part_1002 )
    eav_map.add ( 1003 , part_1003 )
    eav_map.add ( 1004 , part_1004 )
    eav_map.add ( 1005 , part_1005 )
    eav_map.add ( 1006 , code_1006 )
    eav_map.add ( 1007 , code_1007 )
    eav_map.add ( 1008 , code_1008 )
    eav_map.add ( 1009 , code_1009 )
    eav_map.add ( 1010 , code_1010 )
    eav_map.add ( 1011 , code_1011 )

    code_gp_1 = [ name_1009 , name_1006 ]
    code_gp_2 = [ name_1010 , name_1007 ]
    code_gp_3 = [ name_1008 , name_1011 ]

    dict_gp_1003 = { name_1003: code_gp_1 }
    dict_gp_1004 = { name_1004: code_gp_2 }
    dict_gp_1005 = { name_1005: code_gp_3 }

    code_gp_4 = [ dict_gp_1003 , dict_gp_1004 ]
    code_gp_5 = [ dict_gp_1004 , dict_gp_1005 ]

    dict_gp_1001 = { name_1001: code_gp_4 }
    dict_gp_1002 = { name_1002: code_gp_5 }

    dict_map = { name_1000: [ dict_gp_1001 , dict_gp_1002 ] }


    part_1000.add_child( 1001 )
    part_1000.add_child( 1002 )

    part_1001.add_child( 1003 )
    part_1001.add_child( 1004 )
    part_1001.add_parent( 1000 )

    part_1002.add_child( 1004 )
    part_1002.add_child( 1005 )
    part_1002.add_parent( 1000 )

    part_1003.add_child( 1009 )
    part_1003.add_child( 1006 )
    part_1003.add_parent( 1001 )

    part_1004.add_child( 1010 )
    part_1004.add_child( 1007 )
    part_1004.add_parent( 1001 )
    part_1004.add_parent( 1002 )

    part_1005.add_child( 1008 )
    part_1005.add_child( 1011 )
    part_1005.add_parent( 1002 )

    code_1006.add_parent( 1003 )
    code_1007.add_parent( 1004 )
    code_1008.add_parent( 1005 )
    code_1009.add_parent( 1003 )
    code_1010.add_parent( 1004 )
    code_1011.add_parent( 1005 )


    attributes_db_1003 = [[ 14 , '0', 0],
                  [ 1 , 'LP-1003', 1],
                  [ 12 , 'R wave dur L-AVR', 0],
                  [ 11 , '2', 0],
                  [ 10 , 'ACTIVE', 0]]

    attributes_1003  = {'Common rank': '0' ,
                    'Short name': 'R wave dur L-AVR' ,
                    'Class type': '2' ,
                    'Status': 'ACTIVE' ,
                    'Name': 'LP-1003'}

    children_1003 = { 1006 , 1009 }
    parents_1003 = { 1001 }


    for attribute in attributes_1003:
        part_1003.add_attribute( attribute, attributes_1003[ attribute] )


    defining_attribute_id_1003 = 3
    defining_attribute_1003 = 3 , '1003'

    defining_attribute_name_1003 = 'LOINC Part Code'
    defining_attribute_value_1003 = '1003'
    preferred_id_1003 = 'Name'
    code_1003 = 'LP-1003'

    dict_1003 = {'defining definition': 'LOINC Part Code', 'LOINC Part Code': '1003', 'preferred attribute': 'Name', 'Name': 'LP-1003', 'parents': [ 'LOINC Part Code: 1001, LP-1001' ], 'children': [ 'code: 1006, L-1006' , 'code: 1009, L-1009' ]}


    dict_1001 = {'defining definition': 'LOINC Part Code', 'LOINC Part Code': '1001', 'preferred attribute': 'Name',
                 'Name': 'LP-1001', 'parents': ['LOINC Part Code: 1000, LP-1000'],
                 'children': ['code: 1003, L-1003' ]}

    dict_1006 = {'defining definition': 'LOINC Code', 'LOINC Code': '1006', 'preferred attribute': 'Name',
                 'Name': 'LP-1006', 'parents': ['LOINC Part Code: 1003, LP-1003'], 'children': []}

    dict_1009 = {'defining definition': 'LOINC Code', 'LOINC Code': '1009', 'preferred attribute': 'Name',
                 'Name': 'LP-1009', 'parents': ['LOINC Part Code: 1003, LP-1003'], 'children': []}

    dict_1007 = {'defining definition': 'LOINC Code', 'LOINC Code': '1007', 'preferred attribute': 'Name',
                 'Name': 'LP-1007', 'parents': ['LOINC Part Code: 1004, LP-1004'], 'children': []}

    dict_1010 = {'defining definition': 'LOINC Code', 'LOINC Code': '1010', 'preferred attribute': 'Name',
                 'Name': 'LP-1010', 'parents': ['LOINC Part Code: 1004, LP-1004'], 'children': []}

    json_1003 = {"defining definition": "LOINC Part Code", "LOINC Part Code": "1003", "preferred attribute": "Name", "Name": "LP-1003", "parents": ["LOINC Part Code: 1001, LP-1001"], "children": ["code: 1006, L-1006", "code: 1009, L-1009"]}

# --------------------------------------------------------

    # --------------------------------------------------------------------------

    # query and method returns
    return_of_obj_id_query = [[0, 1, "10000-9"]]

    return_of_attribute_query = [(0, 14, '0', 0),
                         (0, 13, 'R wave duration in lead AVR', 1),
                         (0, 12, 'R wave dur L-AVR', 0),
                         (0, 11, '2', 0),
                         (0, 10, 'ACTIVE', 0)]


    return_of_attribute_method = [(14, '0', 0),
                          (13, 'R wave duration in lead AVR', 1),
                          (12, 'R wave dur L-AVR', 0),
                          (11, '2', 0),
                          (10, 'ACTIVE', 0)]


    return_of_empty_attribute_query = []

    return_of_empty_attribute_method = []


    return_of_parents_query = [[10, 0],
                         [20, 0],
                         [30, 0],
                         [40, 0],
                         [50, 0]]

    return_of_parents_method = {10, 20, 30, 40, 50}


    return_of_children_query = [[10, 100],
                         [10, 200],
                         [10, 300],
                         [10, 400],
                         [10, 500]]

    return_of_children_method = {100, 200, 300, 400, 500}


    return_of_ancestor_query = [[10], [20], [30]]

    return_of_ancestor_method = {10, 20, 30}


    return_of_ancestor_level_query = [[10, 1],
                         [20, 2],
                         [30, 3],
                         [40, 4]]

    return_of_ancestor_level_method = {10, 20, 30 }


    return_of_descendant_query = [[33], [32],
                         [22], [21], [24], [21],
                         [5], [6], [7],
                         [1], [2]]

    return_of_descendant_method = {33, 32, 22, 21, 24, 1, 2, 5, 6, 7}