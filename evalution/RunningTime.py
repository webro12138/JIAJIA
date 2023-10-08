from evalution.Metric import Metric
class RuningTime(Metric):
    def __init__(self, verbose=True):
        super().__init__()
        self._verbose=verbose
        
    def __call__(self, network, k):
        self._alg(network, k)
        
        return self._alg.running_time()

        