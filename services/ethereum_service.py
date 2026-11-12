from web3 import Web3
from services.blockchain_api import BlockchainAPI

class EthereumService:
    def __init__(self):
        self.api = BlockchainAPI()

    def get_transaction(self, chain: str, tx_hash: str):
        rpc = self.api.evm_rpc(chain)
        if not rpc:
            raise RuntimeError(f"No RPC URL configured for {chain}; add it to .env")
        w3 = Web3(Web3.HTTPProvider(rpc, request_kwargs={"timeout": 15}))
        if not w3.is_connected():
            raise RuntimeError(f"Cannot connect to {chain} RPC")
        tx = w3.eth.get_transaction(tx_hash)
        receipt = w3.eth.get_transaction_receipt(tx_hash)
        return {
            "txid": tx_hash,
            "timestamp": None,
            "inputs": [{"address": tx["from"], "value": int(tx["value"])}],
            "outputs": [{"address": tx["to"], "value": int(tx["value"])}] if tx["to"] else [],
            "confirmed": receipt["status"] == 1,
            "block_number": int(tx["blockNumber"]) if tx["blockNumber"] is not None else None,
            "source": f"{chain}-rpc",
        }
