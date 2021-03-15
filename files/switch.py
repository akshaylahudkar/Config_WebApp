from files.ValidationFunctions import ValidationFunctions

ob1 = ValidationFunctions()


class Validation(object):
    def f(self,AttributeValue,Attribute_type):

        if Attribute_type =='IPv4':
            return ob1.validIPAddress(AttributeValue,'IPv4')
        elif Attribute_type == 'IPv6':
            return ob1.validIPAddress(AttributeValue, 'IPv6')
        elif Attribute_type =='NUMBER':
            return ob1.PositiveNumber(AttributeValue)
        elif Attribute_type == 'NAME':
            return ob1.is_valid_hostname(AttributeValue)
        elif Attribute_type == 'DATE':
            return ob1.isValidDate(AttributeValue)
        elif Attribute_type == 'FILE_PATH':
            return ob1.is_valid_filepath(AttributeValue)
        elif Attribute_type == 'YES/NO':
            return ob1.is_valid_yesNo(AttributeValue)
        elif Attribute_type == 'Not Available':
            return True


