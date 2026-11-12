# CryptoTrace implementation scope

This package is a runnable foundation and synthetic demonstration, not a finished commercial chain analytics platform.
The API currently supports:
- Synthetic four-transaction peel-chain/mixer/dust scenario
- Bitcoin single-address transaction fetch and single-tx lookup via Blockstream Esplora
- EVM transaction/receipt lookup on configured Ethereum, Polygon, BNB Chain, Arbitrum and Base RPCs
- NetworkX directed graph, baseline pattern flags, ranked terminal nodes
- PostgreSQL trace persistence and SHA-256 hash-chained local audit file
- PyVis graph HTML generation and pytest + HTTPX test client

Not yet implemented as production-grade capabilities:
- Recursive multi-hop live chain crawling for BTC/EVM
- Cross-chain bridge event correlation/indexing
- Real-world deanonymization or person identity resolution
- Sanctions/ransomware/entity intelligence feeds
- Durable end-to-end RabbitMQ worker execution, Redis cache integration, Neo4j graph writes
- Formal Alembic migration revisions, user authentication, authorization and tenant isolation

These limits are intentional: the API does not claim functionality that would otherwise create misleading forensic results.
