# --------------------------------------------------------------------------------------------
# --------------------------------------------------------------------------------------------

class AttributeTypeDefinition:
    """
    Represents one row of the attribute_type_definitions table
    """


    # ------------------------------------------------

    def __init__(self, attribute_id , attribute_name , attribute_type ):
        """

        :param attribute_id: integer used in schemas for this type
        :param attribute_name: name used for this type in schema, LOINC Code
        :param attribute_type: type for this attribute using attribute_type ENUM, name, value, etc.
        """

        self.attribute_id = attribute_id
        self.attribute_name = attribute_name
        self.attribute_type = attribute_type


    # ------------------------------------------------

    def get_attribute_id( self ): return self.attribute_id
    def get_attribute_name( self ): return self.attribute_name
    def get_attribute_type( self ): return self.attribute_type


    # ------------------------------------------------


