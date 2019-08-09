

class proxy():
    __slots__ = ['ip', 'port', 'points']
    def __init__(self, ip, port, points=1):
        self.ip = ip
        self.port = port
        self.points = points

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

    def __eq__(self, other):
        return self.get_string_address() == other.get_string_address()


if __name__ == '__main__':
    x1 = proxy(123, 45, points=3)
    y = [x1]
    x2 = proxy(123, 452, points=3)
    print(x2 in y)