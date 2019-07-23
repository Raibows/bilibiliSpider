

class proxy():
    def __init__(self, ip, port):
        self.ip = ip
        self.port = port
        self.points = 1

    def __get_raw_address(self):
        address = f'{self.ip}:{self.port}'
        return address

    def get_dict_address(self):
        address = {
            "http": "http://{}".format(self.__get_raw_address())
        }
        return address

    def get_string_address(self):
        address = f'http://{self.__get_raw_address()}'
        return address

    def __gt__(self, other):
        return True if self.points > other.points else False

    def __repr__(self):
        return self.__get_raw_address()