# CryptoTrace Backend

Cybersecurity-oriented blockchain transaction forensics prototype using FastAPI, PostgreSQL, Neo4j, Redis, RabbitMQ, NetworkX, scikit-learn, PyVis and web3.py.

## Important scope and evidence warning

CryptoTrace produces heuristic investigative leads from public blockchain data. It does **not** identify a person behind a wallet, prove criminal activity, or establish legal attribution. Mixer/bridge labels and real-world entity labels require trusted, curated intelligence datasets; none are fabricated or bundled. The sample scenario is synthetic and all sample wallet identifiers are fictional.

The current implementation provides a working sample-data trace, Bitcoin address/transaction ingestion through the free Blockstream Esplora API, one-transaction EVM RPC lookup for Ethereum/Polygon/BNB Chain/Arbitrum/Base, graph construction, baseline heuristics, ranked terminal wallets, security flags, persistence, and hash-chained audit logging. A true multi-hop live EVM indexer, complete Bitcoin recursive crawler, production attribution feeds, and asynchronous distributed trace pipeline are extension points—not falsely represented as complete features.

## Requirements

- Python 3.11 or 3.12 recommended
- Docker Desktop with WSL2 on Windows, or Docker Engine on Linux
- VS Code + REST Client extension (for `requests.http`)

## 1. Start infrastructure

From the `CryptoTrace/backend` folder:

```bash
docker compose up -d
docker compose ps
```

Services:
- PostgreSQL: `localhost:5432` (database `cryptotrace`)
- Redis: `localhost:6379`
- RabbitMQ: `localhost:5672`; management UI `http://localhost:15672`
- Neo4j: browser `http://localhost:7474`; Bolt `localhost:7687`

Default local development credentials are in `.env`. Change them before exposing services or deploying.

## 2. Create Python environment

### Windows PowerShell

```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
```

If PowerShell blocks activation, run:
```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\.venv\Scripts\Activate.ps1
```

### Ubuntu / WSL / macOS

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
```

## 3. Configure environment

`.env` is included with local development defaults. `DATA_MODE=sample` means the first run needs no API keys or paid services. Copy `.env.example` for reference. For live EVM reads, add a free RPC URL for the chain you want to query. For live Bitcoin reads, Blockstream Esplora is configured by default and does not require an API key.

Supported EVM RPC variables:
`ETHEREUM_RPC_URL`, `POLYGON_RPC_URL`, `BSC_RPC_URL`, `ARBITRUM_RPC_URL`, `BASE_RPC_URL`.

Free RPC plans have quotas and may change; use your provider's documented endpoint and keep keys private. Never commit `.env`.

## 4. Run API

```bash
uvicorn main:app --reload --host 127.0.0.1 --port 8000
```

Open:
- Swagger: http://127.0.0.1:8000/docs
- Health: http://127.0.0.1:8000/health

## 5. Test the API

Open `requests.http` in VS Code and click **Send Request** above the requests. First run the synthetic sample request. It stores the trace in PostgreSQL and writes an audit event to `logs/audit_log.jsonl`.

Then use the returned `trace_id` in the report, graph and receiver endpoints.

## 6. Run tests

```bash
pytest -q
```

## 7. Useful endpoints

| Method | Endpoint | Purpose |
|---|---|---|
| GET | `/health` | Health check |
| POST | `/api/v1/traces` | Start a trace |
| GET | `/api/v1/graphs/{trace_id}` | Retrieve graph |
| POST | `/api/v1/graphs/{trace_id}/visualize` | Generate PyVis HTML |
| GET | `/api/v1/risk/{trace_id}/receivers` | Ranked terminal wallets |
| GET | `/api/v1/reports/{trace_id}` | Investigation summary |
| GET | `/api/v1/security/audit/verify` | Verify hash chain |
| GET | `/api/v1/audit` | Recent audit records |

## Data and heuristic notes

- Bitcoin live mode uses Blockstream Esplora. It currently fetches one address's returned transactions or one transaction by txid; it does not recursively crawl every hop from live chain history.
- EVM live mode fetches one transaction and receipt from the configured RPC. Full address history needs an indexed data provider or self-hosted indexer.
- Common-input ownership is a Bitcoin-only heuristic and is not applied to EVM.
- Mixer, peel-chain, dusting and look-alike detections are indicators, not conclusive classifications.
- Address similarity is a warning for manual review, not a claim that two wallets are controlled by the same person.
- No sanctions/ransomware/exchange address list is included. Add curated, source-attributed labels and record dataset provenance before operational use.
- `max_hops` is recorded as a request parameter; the synthetic demo includes four transaction steps. Recursive live traversal is a planned extension.
- PostgreSQL is the source of truth. Redis, RabbitMQ and Neo4j containers are included and connection modules are supplied; this initial API path does not yet require those services to respond to complete a sample trace.

## Stop containers

```bash
docker compose down
```

Delete local database volumes (destructive):
```bash
docker compose down -v
```

## Before production

Add authentication/authorization, per-user rate limits, secrets management, TLS, provider retry/backoff, Alembic migration review, durable worker orchestration, curated intelligence provenance, immutable/off-host audit backups, observability, and legal/compliance review. Do not expose the development credentials or unauthenticated API publicly.
