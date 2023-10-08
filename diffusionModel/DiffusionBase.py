import networkx as nx

class Weighter(object):

    def assign_weights(self, network, regen=False):
        if(network._type_of_weight != self.__class__.__name__ or regen):
            network.set_type_of_weight(self.__class__.__name__)
            self.assign_active_prob(network)
            self.assign_active_threhsold(network)

    def assign_active_prob(self, network):
        pass

    def get_active_prob(self, network, edge):
        pass

    def assign_active_threhsold(self, network):
        pass

    def get_threhsold(self, network, node):
        pass

class DiffusionBase(object):
    def __init__(self):
        self._S = None
        self._weighter = None
 
    def __call__(self,network, S:list):
        self.set_S(S)
        return self.simulate(network, S)

    def set_verbose(self, verbose):
        self._verbose = verbose

    def set_S(self, S):
        assert isinstance(S, list), "S的类型必须时list"
        assert len(S) == len(set(S)), "S不能存在相同元素"
        self._S = S

    def set_network(self, network):
        self._network = network

    def cal_gain(self, network, S:list, v):
        self.set_network(network)
        self._weighter.assign_weights(network)
        self.set_S(S)
        a = self.simulate(network, S)
        self.set_S(S + [v])
        b = self.simulate(network, S + [v])
        return b - a

    def simulate(self, network, S):
        pass

    def step(self):
        pass
    
    def approx_func(self, network, S):
        pass