from services.blockchain_api import BlockchainAPI

class BitcoinService:
    def __init__(self):
        self.api = BlockchainAPI()

    async def fetch_address(self, address: str, limit: int = 30):
        txs = await self.api.bitcoin_address_txs(address)
        return [self.normalize_tx(tx) for tx in txs[:limit]]

    async def fetch_transaction(self, txid: str):
        return self.normalize_tx(await self.api.bitcoin_tx(txid))

    @staticmethod
    def normalize_tx(tx):
        txid = tx.get("txid")
        if not isinstance(txid, str) or len(txid) != 64:
            raise ValueError("Malformed transaction returned by provider")
        outputs = tx.get("vout", [])
        inputs = tx.get("vin", [])
        return {
            "txid": txid,
            "timestamp": (tx.get("status") or {}).get("block_time"),
            "inputs": [{"address": i.get("prevout", {}).get("scriptpubkey_address"), "value": i.get("prevout", {}).get("value", 0)} for i in inputs if i.get("prevout")],
            "outputs": [{"address": o.get("scriptpubkey_address"), "value": o.get("value", 0)} for o in outputs],
            "confirmed": (tx.get("status") or {}).get("confirmed", False),
            "source": "blockstream-esplora",
        }
