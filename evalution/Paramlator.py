from algorithm import PSOBMIM
import itertools
import numpy as np
from network import Network
class Paramlator:
    def __init__(self, metric, networks, k, alg) -> None:
        self._alg = alg
        self._metric = metric
        self._networks = networks
        self._k = k
    def __call__(self, type="cons", **kwds):
        assert type in ["cons", "all"], "type 必须是cons或all"
        result = {}
        result["config"] = dict(kwds)
        result["result"] = {}   
        
        for network in self._networks:
            result["result"][network.get_name()] = []
            if(type == "cons"):
                param_combinations = zip(*kwds.values())
            else:
                param_combinations = itertools.product(*(kwds.values())) 

            for params in param_combinations:          

                arg = dict(zip(kwds.keys(), params))
                for key in arg:
                    self._alg.__setattr__(key, arg[key])
                    print(self._alg.beta)
                result["result"][network.get_name()].append(self._metric(network, self._alg(network, self._k)))
            print(f">>在数据集{network.get_name()}调参完成")
        return result

    def set_networks(self, networks):
        assert isinstance(networks, list) and len(networks) != 0, "networks 必须是一个有内容的list"
        assert isinstance(networks[0], Network), "networks 必须是一个Network网络的集合"
        self._networks = networks

    def set_alg(self, alg):
        self._alg = alg