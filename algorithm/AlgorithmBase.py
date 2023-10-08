import time
class AlgorithmBase(object):
    '''
    算法基类
    '''
    def __init__(self):
        '''
        初始化算法基类
        '''
        self._name = self.__class__.__name__
        self._running_time = 0
        self._attr_range = None
        self._verbose = True

    def __call__(self, network, k):
        '''
        调用算法
        '''
        self.change_attr_by_network(network)
        start = time.time()
        S = self.run(network, k)
        end = time.time()
        self._running_time = end - start
        if(self._verbose):
            print(f">>算法{self._name}在{network.get_name()}网络上完成")
        return S
    
    def set_name(self, name):
        '''
        设置算法的名称
        '''
        self._name = name
        
    def get_name(self):
        '''
        获取算法的名称
        '''
        return self._name
    
    def run(self):
        pass

    def change_attr_by_network(self, network):
        '''
        改变算法参数
        '''
        if(self._attr_range is not None):
            for key in self._attr_range:
                if(network.get_name() == key):
                    for key1 in self._attr_range[key]:
                        self.__setattr__(key1, self._attr_range[key][key1])
        
    def set_changed_attr_by_network(self, attr_range):
        self._attr_range = attr_range
        
    def running_time(self):
        '''
        获取算法运行时间
        '''
        return self._running_time
