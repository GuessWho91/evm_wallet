from enum import Enum
import json
from pathlib import Path


class Chains(Enum):

    ETHEREUM = 1
    OPTIMISM = 10
    BSC = 56
    POLYGON = 137
    BASE = 183
    OPBNB = 204
    FANTOM = 250
    ZKSYNC = 324
    ARBITRUM = 42161
    AVALANCHE = 43114
    LINEA = 59144

    BERA_TEST = 80085
    BASE_TEST = 84532
    OPTIMISM_TEST = 11155420
    ARBITRUM_TEST = 421614

    def __init__(self, name):

        script_location = Path(__file__).absolute().parent
        info = open(f'{script_location}/../data/chains_info.json')
        chains_data = json.load(info)

        self.chain_data = chains_data[self.name.lower()]

    def get_rpc(self):
        return self.chain_data["rpc"][0]

    def get_scan_url(self):
        return self.chain_data["explorer"]

    def get_api_url(self):
        return self.chain_data["api"]

    def get_min_gas(self):

        token_name = self.chain_data["token"]

        if token_name == "BNB":
            return 0.0007
        elif token_name == "MATIC":
            return 0.1
        elif token_name == "AVAX" or token_name == "BERA":
            return 0.005
        elif token_name == "ETH":
            return 0.0001
        elif token_name == "FTM":
            return 0.3

    def get_main_coin(self):

        from evm_wallet.coins import BNB, MATIC, ETH, AVAX, FTM, BERA

        token_name = self.chain_data["token"]

        if token_name == "BNB":
            return BNB(self)
        elif token_name == "MATIC":
            return MATIC(self)
        elif token_name == "AVAX":
            return AVAX(self)
        elif token_name == "FTM":
            return FTM(self)
        elif token_name == "ETH":
            return ETH(self)
        elif token_name == "BERA":
            return BERA(self)
