from chains import Chains
from coins import Coin
from w3wallet import Wallet
from w3error import W3Error

from abc import ABC


class W3Transactor(ABC):

    chain: Chains
    wallet: Wallet

    def check_gas(self):
        balance = self.wallet.get_balance()

        if balance["balance"] < self.chain.get_min_gas():
            raise W3Error(f"Not enough gas on wallet {self.wallet.address} in {self.chain}")

    def approve_token_if_need(self, token: Coin, amount_wei, contract_address):
        if not token.get_address() == self.chain.get_main_coin().get_address():
            approved_amount = token.get_approved_amount(self.wallet.web3, self.wallet.address, contract_address)
            if approved_amount < amount_wei:
                token.approve(self.wallet, contract_address, amount_wei, self.wallet.private_key)

    def approve_max_token(self, token: Coin, contract_address):
        approved_amount = token.get_approved_amount(self.wallet.web3, self.wallet.address, contract_address)
        if approved_amount <= token.max_approval_check_int:
            token.approve(self.wallet, contract_address, token.max_approval_int,
                          self.wallet.private_key)
