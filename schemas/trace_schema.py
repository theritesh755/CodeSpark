from pydantic import BaseModel, Field, field_validator
from typing import Literal

class TraceRequest(BaseModel):
    subject: str = Field(min_length=10, max_length=128, description="Wallet address or transaction hash")
    chain: Literal["bitcoin","ethereum","polygon","bsc","arbitrum","base"] = "bitcoin"
    max_hops: int = Field(default=3, ge=1, le=5)
    limit: int = Field(default=30, ge=1, le=100)
    use_sample: bool = True

    @field_validator("subject")
    @classmethod
    def clean_subject(cls, value):
        value = value.strip()
        if any(ord(c) < 32 for c in value):
            raise ValueError("Control characters are not allowed")
        return value
