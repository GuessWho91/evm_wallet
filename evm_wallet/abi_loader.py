from chains import Chains

import requests
import json


class AbiLoader:

    chain: Chains

    def __init__(self, chain):
        self.chain = chain

    def get_abi(self, contract_address):

        abi_endpoint = f'{self.chain.get_api_url()}api?module=contract&action=getabi&address={contract_address}'

        response = requests.get(abi_endpoint)
        response_json = response.json()
        abi_json = json.loads(response_json['result'])
        result = json.dumps(abi_json, indent=4, sort_keys=True)

        return result
