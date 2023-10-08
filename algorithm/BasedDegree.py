from algorithm import AlgorithmBase
class BasedDegree(AlgorithmBase):
    def __init__(self, verbose=True):
        super().__init__()
        self._verbose = verbose
    
    
    def run(self, network, k):
        degrees = network.degrees() #有向图是出度、无向图是度、多层网络是多层度之和
        degrees = sorted(degrees.items(), key = lambda x:x[1], reverse=True)
        S = []
        for i in range(k):
            S.append(degrees[i][0])
        return S
