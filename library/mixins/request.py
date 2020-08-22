class RequestMixin:
    __request = None

    @property
    def request(self):
        return self.__request

    @request.setter
    def request(self, value):
        self.__request = value
