from evalution.Metric import Metric
class InfluenceSpread(Metric):
    def __init__(self, diffusion_model, verbose=True):
        super().__init__()
        self._verbose=verbose
        self._diffusion_model = diffusion_model
    
    def __call__(self, network, S):
        self._diffusion_model.set_verbose(self._verbose)
        return self._diffusion_model(network, S)

        