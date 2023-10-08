class Metric:

    def __init__(self):
        self._name = self.__class__.__name__

    def get_name(self):
        return self._name
    
    def set_name(self, name):
        self._name = name

    def __call__(network, S):
        pass        