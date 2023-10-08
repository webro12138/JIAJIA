from constant import NETWORK_DATASETS
class NODATASETException(Exception):
    """
    但没有发现指定数据集时抛出错误
    """

    def __init__(self, name):
        self.message = f"为发现数据集{name}"
        self.message += ",请检查数据集名称是否正确. 本baockend支持的数据集有:"
        for name in NETWORK_DATASETS:
            self.message += f"{name},"
        self.message = self.message[:-1]
        
    def __str__(self):
        return self.message