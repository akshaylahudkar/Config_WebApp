import re
from datetime import datetime

class ValidationFunctions(object):
    def validIPAddress(self, IP, IPType):
        """
      :type IP: str
      :rtype: str
      """

        def isIPv4(s):
            try:
                return str(int(s)) == s and 0 <= int(s) <= 255
            except:
                return False

        def isIPv6(s):
            if len(s) > 4:
                return False
            try:
                return int(s, 16) >= 0 and s[0] != '-'
            except:
                return False

        if IPType == 'IPv4' and IP.count(".") == 3 and all(isIPv4(i) for i in IP.split(".")):
            return True
        if IPType == 'IPv6' and IP.count(":") == 7 and all(isIPv6(i) for i in IP.split(":")):
            return True
        return False

    def PositiveNumber(self, AttributeValue):
        try:
            int(AttributeValue)
            return True
        except ValueError:
            return False

    def is_valid_hostname(self,name):

        if len(name) > 253:
            return False
        try:
            if int(name):
                return False
        except:
            return bool(re.match(r"^[ A-Za-z0-9_@/+-]*$", name))


    def isValidDate(self,AttributeValue):

        try:
            print('in try')
            date = datetime.strptime(AttributeValue, '%d-%m-%Y')
            return True
        except ValueError:
            print("date exception ")
            return False

    def is_valid_filepath(self, filename):

        if filename[-1] == '/':
            return False

        return bool(re.match(r"^/|(/[a-zA-Z0-9_-]+)+$", filename))



    def is_valid_yesNo(self, attribute):

        if attribute == 'YES' or attribute == 'NO':
            return True
        return False


