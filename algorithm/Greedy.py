from algorithm import AlgorithmBase
from tqdm import tqdm
class Greedy(AlgorithmBase):
    def __init__(self, diffusion_model, verbose=True):
        super().__init__()
        self._diffusion_model = diffusion_model
        self._diffusion_model.set_verbose(False)
        self._verbose = verbose
        
    def run(self, network, k):
        assert isinstance(k, int), "k是一个正整数"
        self._diffusion_model.set_network(network)
        S = []
        loops = tqdm(range(k))
        allnodes = network.nodes()
        for _ in loops:
            temp = [(node, self._diffusion_model.cal_gain(network, S, node)) for node in set(allnodes) - set(S)]
            s = max(temp, key = lambda x:x[1])[0]
            S.append(s)
            loops.set_description(f"选择种子 | 选中 {s}")
        return S
