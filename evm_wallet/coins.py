from evm_wallet.w3utils import sleep
from evm_wallet.chains import Chains

from pathlib import Path

import json
import random

erc20_abi = '[{"constant":true,"inputs":[],"name":"name","outputs":[{"name":"","type":"string"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"name":"_upgradedAddress","type":"address"}],"name":"deprecate","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":false,"inputs":[{"name":"_spender","type":"address"},{"name":"_value","type":"uint256"}],"name":"approve","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[],"name":"deprecated","outputs":[{"name":"","type":"bool"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"name":"_evilUser","type":"address"}],"name":"addBlackList","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[],"name":"totalSupply","outputs":[{"name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"name":"_from","type":"address"},{"name":"_to","type":"address"},{"name":"_value","type":"uint256"}],"name":"transferFrom","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[],"name":"upgradedAddress","outputs":[{"name":"","type":"address"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[{"name":"","type":"address"}],"name":"balances","outputs":[{"name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"decimals","outputs":[{"name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"maximumFee","outputs":[{"name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"_totalSupply","outputs":[{"name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[],"name":"unpause","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[{"name":"_maker","type":"address"}],"name":"getBlackListStatus","outputs":[{"name":"","type":"bool"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[{"name":"","type":"address"},{"name":"","type":"address"}],"name":"allowed","outputs":[{"name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"paused","outputs":[{"name":"","type":"bool"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[{"name":"who","type":"address"}],"name":"balanceOf","outputs":[{"name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[],"name":"pause","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[],"name":"getOwner","outputs":[{"name":"","type":"address"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"owner","outputs":[{"name":"","type":"address"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"symbol","outputs":[{"name":"","type":"string"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"name":"_to","type":"address"},{"name":"_value","type":"uint256"}],"name":"transfer","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":false,"inputs":[{"name":"newBasisPoints","type":"uint256"},{"name":"newMaxFee","type":"uint256"}],"name":"setParams","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":false,"inputs":[{"name":"amount","type":"uint256"}],"name":"issue","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":false,"inputs":[{"name":"amount","type":"uint256"}],"name":"redeem","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[{"name":"_owner","type":"address"},{"name":"_spender","type":"address"}],"name":"allowance","outputs":[{"name":"remaining","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"basisPointsRate","outputs":[{"name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[{"name":"","type":"address"}],"name":"isBlackListed","outputs":[{"name":"","type":"bool"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"name":"_clearedUser","type":"address"}],"name":"removeBlackList","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[],"name":"MAX_UINT","outputs":[{"name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"name":"newOwner","type":"address"}],"name":"transferOwnership","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":false,"inputs":[{"name":"_blackListedUser","type":"address"}],"name":"destroyBlackFunds","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"inputs":[{"name":"_initialSupply","type":"uint256"},{"name":"_name","type":"string"},{"name":"_symbol","type":"string"},{"name":"_decimals","type":"uint256"}],"payable":false,"stateMutability":"nonpayable","type":"constructor"},{"anonymous":false,"inputs":[{"indexed":false,"name":"amount","type":"uint256"}],"name":"Issue","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"name":"amount","type":"uint256"}],"name":"Redeem","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"name":"newAddress","type":"address"}],"name":"Deprecate","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"name":"feeBasisPoints","type":"uint256"},{"indexed":false,"name":"maxFee","type":"uint256"}],"name":"Params","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"name":"_blackListedUser","type":"address"},{"indexed":false,"name":"_balance","type":"uint256"}],"name":"DestroyedBlackFunds","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"name":"_user","type":"address"}],"name":"AddedBlackList","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"name":"_user","type":"address"}],"name":"RemovedBlackList","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"name":"owner","type":"address"},{"indexed":true,"name":"spender","type":"address"},{"indexed":false,"name":"value","type":"uint256"}],"name":"Approval","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"name":"from","type":"address"},{"indexed":true,"name":"to","type":"address"},{"indexed":false,"name":"value","type":"uint256"}],"name":"Transfer","type":"event"},{"anonymous":false,"inputs":[],"name":"Pause","type":"event"},{"anonymous":false,"inputs":[],"name":"Unpause","type":"event"}]'


def get_random_coin():
    coins = (USDT, USDC)
    return random.choice(coins)()


class Coin:
    abi = ""
    chain: Chains

    def __init__(self, chain):
        self.chain = chain

        script_location = Path(__file__).absolute().parent
        info = open(f'{script_location}/../data/coins_info.json')
        coins_data = json.load(info)
        self.coin_data = coins_data[self.__class__.__name__]
        if self.coin_data is None:
            raise Exception(f"Cant load info of {self.__class__.__name__} coin")

        max_approval_hex = f"0x{64 * 'f'}"
        self.max_approval_int = int(max_approval_hex, 16)
        max_approval_check_hex = f"0x{15 * '0'}{49 * 'f'}"
        self.max_approval_check_int = int(max_approval_check_hex, 16)

    def get_address(self):
        coin_address = self.coin_data[self.chain.name.lower()]
        if self.coin_data is None:
            raise Exception(f"Cant load address of {self.__class__.__name__} coin in {self.chain.name.lower()} chain")
        else:
            return coin_address

    def get_balance(self, web3, address):

        token_contract = self.__load_contract__(web3)
        balance = token_contract.functions.balanceOf(address).call()  # returns int with balance, without decimals
        human_readable = web3.from_wei(balance, 'ether')

        return human_readable

    def _addr_to_str(a, web3) -> str:
        if isinstance(a, bytes):
            # Address or ChecksumAddress
            addr: str = web3.to_checksum_address("0x" + bytes(a).hex())
            return addr
        elif isinstance(a, str) and a.startswith("0x"):
            addr = web3.to_checksum_address(a)
            return addr

    def approve(self, wallet, contract_address, max_approval, private_key):

        token_contract = self.__load_contract__(wallet.web3)
        function = token_contract.functions.approve(
            contract_address, max_approval
        )

        wallet.logger.warning(f"Approving coin {self.get_address()} for amount {max_approval}...")
        tx = function.build_transaction({
            'from': wallet.address,
            "value": 0,
            'gasPrice': 50000000000,
            'nonce': wallet.web3.eth.get_transaction_count(wallet.address),
        })

        gas = int(wallet.web3.eth.estimate_gas(tx) * 1.3)
        tx.update({"gas": gas})

        signed_txn = wallet.web3.eth.account.sign_transaction(
            tx, private_key=private_key
        )
        raw_transaction = wallet.web3.eth.send_raw_transaction(signed_txn.rawTransaction)

        wallet.web3.eth.wait_for_transaction_receipt(raw_transaction, timeout=6)

        sleep(1, 3)

    def get_approved_amount(self, web3, address, contract_addr):
        token_contract = self.__load_contract__(web3)
        amount = token_contract.functions.allowance(address, contract_addr).call()

        return amount

    def __load_contract__(self, web3):

        if self.abi == "":
            # self.abi = AbiLoader(self.chain).get_abi(self.get_address())
            self.abi = erc20_abi

        token_contract = web3.eth.contract(address=web3.to_checksum_address(self.get_address()),
                                           abi=self.abi)  # declaring the token contract

        return token_contract


class EMPTY(Coin):
    def get_address(self):
        return "0x0000000000000000000000000000000000000000"


class ETH(Coin):
    pass


class BNB(Coin):
    pass


class USDT(Coin):
    pass


class USDC(Coin):
    pass


class AVAX(Coin):
    pass


class FTM(Coin):
    pass


class MATIC(Coin):
    pass

class BERA(Coin):
    pass
