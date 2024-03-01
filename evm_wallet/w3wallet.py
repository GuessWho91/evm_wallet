import time
import asyncio
from eth_account.messages import encode_defunct

from web3 import Web3
from web3.exceptions import TransactionNotFound

from evm_wallet.coins import erc20_abi
from evm_wallet.logger import W3Logger
from evm_wallet.chains import Chains
from evm_wallet.w3error import W3Error


class Wallet:

    GAS_MULTIPLIER = 1.3
    DEADLINE = int(time.time()) + 10 * 60  # 10 min

    def __init__(self, chain: Chains, private_key: str):
        self.chain = chain
        self.web3 = Web3(Web3.HTTPProvider(chain.get_rpc()))
        self.logger = W3Logger()

        self.private_key = private_key
        pa = self.web3.eth.account.from_key(self.private_key)
        self.address = pa.address

    def get_balance(self):
        balance = self.web3.eth.get_balance(self.address)
        human_readable = self.web3.from_wei(balance, 'ether')

        return {"balance_wei": balance, "balance": human_readable, "symbol":
            self.chain.get_main_coin().__class__.__name__, "decimal": 18}

    def get_token_balance(self, token):

        # erc20_abi = AbiLoader(chain).get_abi(token)
        # declaring the token contract
        contract = self.web3.eth.contract(address=self.web3.to_checksum_address(token.lower()), abi=erc20_abi)

        symbol = contract.functions.symbol().call()
        decimal = contract.functions.decimals().call()
        balance_wei = contract.functions.balanceOf(self.address).call()

        balance = balance_wei / 10 ** decimal

        return {"balance_wei": balance_wei, "balance": balance, "symbol": symbol, "decimal": decimal}

    def get_amount_wei(self, token: str, amount):
        if token.lower() == self.chain.get_main_coin().get_address().lower():
            token_balance = self.get_balance()
        else:
            token_balance = self.get_token_balance(token)

        amount_wei = int(amount * 10 ** token_balance["decimal"])

        if token_balance["balance_wei"] < amount_wei:
            raise W3Error(f"[Wallet][{self.address}] balance of {token_balance['symbol']} in {self.chain} is too low")

        return amount_wei

    def get_current_net(self):
        return self.web3.net.version

    def get_deadline(self):
        return self.DEADLINE

    def get_trans_options(self, amount):
        return {
            "chainId": self.web3.eth.chain_id,
            'from': self.address,
            'value': amount,
            'gasPrice': self.web3.eth.gas_price,
            'nonce': self.web3.eth.get_transaction_count(self.address),
        }

    def get_trans_options_2(self, amount):
        return {
            "chainId": self.web3.eth.chain_id,
            'from': self.address,
            'value': amount,
            'maxFeePerGas': 10024,
            'maxPriorityFeePerGas': 10000,
            'type': 2,
            'nonce': self.web3.eth.get_transaction_count(self.address),
        }

    async def make_tx_by_data(self, data, contract_address, tag, amount=0):
        amount_wei = self.web3.to_wei(amount, 'ether')
        tx_data = self.get_trans_options(amount_wei)
        tx_data.update({"data": data,
                        "to": contract_address})

        gas = int(self.web3.eth.estimate_gas(tx_data) * self.GAS_MULTIPLIER)
        tx_data.update({"gas": gas})

        try:
            tx_hex = await self.sigh_transaction(tx_data)
        except ValueError as e:
            tx_data.update({"nonce": tx_data.get("nonce") + 1})
            tx_hex = await self.sigh_transaction(tx_data)

        self.logger.success(
            f"[{tag}] [{self.address}] Транзакция отправлена {self.chain.get_scan_url()}{tx_hex}")

        await self.wait_until_tx_finished(tx_hex)

        return tx_hex

    async def sigh_transaction(self, txn):

        try:
            gas = int(self.web3.eth.estimate_gas(txn) * self.GAS_MULTIPLIER)  # 250000
            txn.update({"gas": gas})
        except:  # Газ уже назначен
            time.sleep(1)

        signed_txn = self.web3.eth.account.sign_transaction(txn, private_key=self.private_key)
        tx_token = self.web3.eth.send_raw_transaction(signed_txn.rawTransaction)
        tx_hex = self.web3.to_hex(tx_token)

        await self.wait_until_tx_finished(tx_hex)

        return tx_hex

    def sign_message(self, msg):
        message = encode_defunct(text=msg)
        signed_message = self.web3.eth.account.sign_message(message, private_key=self.private_key)
        return signed_message.signature.hex()

    def balance_of_erc721(self, address, contract_address):
        abi = '[{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"owner","type":"address"},{"indexed":true,"internalType":"address","name":"approved","type":"address"},{"indexed":true,"internalType":"uint256","name":"tokenId","type":"uint256"}],"name":"Approval","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"owner","type":"address"},{"indexed":true,"internalType":"address","name":"operator","type":"address"},{"indexed":false,"internalType":"bool","name":"approved","type":"bool"}],"name":"ApprovalForAll","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"from","type":"address"},{"indexed":true,"internalType":"address","name":"to","type":"address"},{"indexed":true,"internalType":"uint256","name":"tokenId","type":"uint256"}],"name":"Transfer","type":"event"},{"inputs":[{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"tokenId","type":"uint256"}],"name":"approve","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"owner","type":"address"}],"name":"balanceOf","outputs":[{"internalType":"uint256","name":"balance","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"tokenId","type":"uint256"}],"name":"getApproved","outputs":[{"internalType":"address","name":"operator","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"owner","type":"address"},{"internalType":"address","name":"operator","type":"address"}],"name":"isApprovedForAll","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"name","outputs":[{"internalType":"string","name":"","type":"string"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"tokenId","type":"uint256"}],"name":"ownerOf","outputs":[{"internalType":"address","name":"owner","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"from","type":"address"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"tokenId","type":"uint256"}],"name":"safeTransferFrom","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"from","type":"address"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"tokenId","type":"uint256"},{"internalType":"bytes","name":"data","type":"bytes"}],"name":"safeTransferFrom","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"operator","type":"address"},{"internalType":"bool","name":"_approved","type":"bool"}],"name":"setApprovalForAll","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"bytes4","name":"interfaceId","type":"bytes4"}],"name":"supportsInterface","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"symbol","outputs":[{"internalType":"string","name":"","type":"string"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"tokenId","type":"uint256"}],"name":"tokenURI","outputs":[{"internalType":"string","name":"","type":"string"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"from","type":"address"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"tokenId","type":"uint256"}],"name":"transferFrom","outputs":[],"stateMutability":"nonpayable","type":"function"}]'

        contract = self.web3.eth.contract(address=self.web3.to_checksum_address(contract_address), abi=abi)
        return contract.functions.balanceOf(address).call()

    async def wait_until_tx_finished(self, hash_str, max_wait_time=60) -> None:
        start_time = time.time()
        while True:
            try:
                receipts =  self.web3.eth.get_transaction_receipt(hash_str)
                status = receipts.get("status")
                if status == 1:
                    self.logger.success(f"[Wallet] [{self.address}] Transaction succeed {hash_str} ")
                    return
                elif status is None:
                    await asyncio.sleep(0.3)
                else:
                    self.logger.error(f"[Wallet] [{self.address}] Transaction failed {hash_str}")
                    return
            except TransactionNotFound:
                if time.time() - start_time > max_wait_time:
                    self.logger.error(f'[Wallet][{self.address}] Transaction failed {hash_str}')
                    return
                await asyncio.sleep(1)
