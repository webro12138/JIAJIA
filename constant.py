import os

# 项目根目录
ROOT_PATH = os.path.dirname(os.path.abspath(__file__))

# 数据目录
DATA_PATH = os.path.join(ROOT_PATH, "data")

# 数据集目录
DATASETS_PATH = os.path.join(ROOT_PATH, "dataset", "data")

# 实验结果目录
RESULT_PATH = os.path.join(ROOT_PATH, "result")

# 支持的多层网络数据集
BASE_MULTILAYER_NETWORK_DATASETS = ["Celegans", "CKM", "Gallus", "LMT", "Rattus", "Mus", "PierreAuger", "SacchPomb", "HumanHIV1", "LMT", "EUAir", "CElegans", "Plasmodium"]

# 支持单层网络数据集
SINGLE_LAYER_NETWORK_DATASETS = ["facebook", "soc-wiki-Vote"]

# LF存储格式的多层网络
LF_MULTILAYER_NETWORK_DATASETS = ["Multi_lastfm_asia", "Multi-Soc-wiki-Vote"]

# 所有支持的网络
NETWORK_DATASETS = SINGLE_LAYER_NETWORK_DATASETS + BASE_MULTILAYER_NETWORK_DATASETS + LF_MULTILAYER_NETWORK_DATASETS


## 我们实验用的数据集
EXP_DATASETS = [ "CElegans", "CKM", "PierreAuger", "Gallus", "Multi-Soc-wiki-Vote", "Multi_lastfm_asia"]