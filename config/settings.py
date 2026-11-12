from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field

class Settings(BaseSettings):
    APP_NAME: str = "CryptoTrace"
    APP_ENV: str = "development"
    API_V1_PREFIX: str = "/api/v1"
    SECRET_KEY: str = "dev-only-change-me"
    CORS_ORIGINS: str = "http://localhost:5173,http://localhost:3000"
    DATABASE_URL: str = "postgresql+psycopg://cryptotrace:cryptotrace_dev@localhost:5432/cryptotrace"
    REDIS_URL: str = "redis://localhost:6379/0"
    RABBITMQ_URL: str = "amqp://cryptotrace:cryptotrace_dev@localhost:5672/"
    NEO4J_URI: str = "bolt://localhost:7687"
    NEO4J_USERNAME: str = "neo4j"
    NEO4J_PASSWORD: str = "cryptotrace_dev_password"
    BLOCKSTREAM_BASE_URL: str = "https://blockstream.info/api"
    ETHEREUM_RPC_URL: str = ""
    POLYGON_RPC_URL: str = ""
    BSC_RPC_URL: str = ""
    ARBITRUM_RPC_URL: str = ""
    BASE_RPC_URL: str = ""
    ETHERSCAN_API_KEY: str = ""
    POLYGONSCAN_API_KEY: str = ""
    BSCSCAN_API_KEY: str = ""
    ARBISCAN_API_KEY: str = ""
    BASESCAN_API_KEY: str = ""
    DATA_MODE: str = "sample"
    HTTP_TIMEOUT_SECONDS: int = 15
    MAX_TRACE_HOPS: int = Field(default=5, ge=1, le=10)
    MAX_TRANSACTIONS_PER_ADDRESS: int = 50
    RISK_HIGH_THRESHOLD: int = 70
    LOG_LEVEL: str = "INFO"

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    @property
    def cors_origins(self):
        return [x.strip() for x in self.CORS_ORIGINS.split(",") if x.strip()]

settings = Settings()
