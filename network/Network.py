class Network(object):
    def __init__(self):
        self._type_of_weight = None
        self._name = self.__class__.__name__
    
    def set_type_of_weight(self, type_of_weight):
        self._type_of_weight = type_of_weight
    
    def set_name(self, name):
        self._name = name

    def get_name(self):
        return self._name

    def nodes(self):
        return self._nodes

    def number_of_nodes(self):
        pass

    def number_of_edges(self):
        pass

    def degrees(self):
        pass
    
    
   
    