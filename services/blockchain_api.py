import httpx
from config.settings import settings

class BlockchainAPI:
    def __init__(self):
        self.timeout = settings.HTTP_TIMEOUT_SECONDS

    async def bitcoin_address_txs(self, address: str):
        url = f"{settings.BLOCKSTREAM_BASE_URL.rstrip('/')}/address/{address}/txs"
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            response = await client.get(url)
            response.raise_for_status()
            payload = response.json()
        if not isinstance(payload, list) or len(payload) > 1000:
            raise ValueError("Unexpected or oversized Blockstream response")
        return payload

    async def bitcoin_tx(self, txid: str):
        url = f"{settings.BLOCKSTREAM_BASE_URL.rstrip('/')}/tx/{txid}"
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            response = await client.get(url)
            response.raise_for_status()
            payload = response.json()
        if not isinstance(payload, dict) or payload.get("txid") != txid:
            raise ValueError("Blockstream transaction identity check failed")
        return payload

    def evm_rpc(self, chain: str):
        return {
            "ethereum": settings.ETHEREUM_RPC_URL,
            "polygon": settings.POLYGON_RPC_URL,
            "bsc": settings.BSC_RPC_URL,
            "arbitrum": settings.ARBITRUM_RPC_URL,
            "base": settings.BASE_RPC_URL,
        }.get(chain, "")
