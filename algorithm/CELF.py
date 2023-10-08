from algorithm import AlgorithmBase
from tqdm import tqdm

class CELF(AlgorithmBase):
    def __init__(self, diffusion_model, verbose=True):
        super().__init__()
        self._diffusion_model = diffusion_model
        self._diffusion_model.set_verbose(False)
        self._verbose = verbose
    
    def run(self, network, k):
        assert isinstance(k, int), "k是一个正整数"
        S = []
        
        theta = {}
        allnodes = network.nodes()

        if(self._verbose):
            loops = tqdm(range(network.number_of_nodes()))
        else:
            loops = range(network.number_of_nodes())

        for i in loops:
            theta[allnodes[i]] = self._diffusion_model.cal_gain(network, [], allnodes[i])
            loops.set_description(f"计算节点IS | 选中 {allnodes[i]}")

        if self._verbose:
            print(">>第一轮影响力扩展度计算完成")

        loops = tqdm(range(k))
        for _ in loops:
            flag = {}
            for node in allnodes:
                flag[node] = False
            
            while True:
                s = max(theta.items(), key=lambda x:x[1])[0]
                if flag[s]:
                    S.append(s)
                    theta[s] = 0
                    loops.set_description(f"选择种子 | 选中 {s}")
                    break
                else:
                    theta[s] = self._diffusion_model.cal_gain(network, S, s)
                    flag[s] = True
        
        return S


        