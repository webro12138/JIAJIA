from algorithm import AlgorithmBase
from tqdm import tqdm
import random
class RandomSelect(AlgorithmBase):
    def __init__(self, verbose=True):
        super().__init__()
        self._verbose = verbose

    def run(self, network, k):
        assert k <= network.number_of_nodes(), "network节点个数小于k"
        S = list(random.sample(network.nodes(), k))
        return S