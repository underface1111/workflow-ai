"""Pydantic contract for AI Test Agent output (Giai đoạn 2 — Bước B)."""

from pydantic import BaseModel, Field, field_validator


class GeneratedUnitTest(BaseModel):
    """Machine-readable response from AI Test Agent."""

    ticket_id: str = Field(..., min_length=1, max_length=64)
    file_name: str = Field(..., pattern=r"^[a-z0-9-]+\.test\.js$")
    file_content: str = Field(..., min_length=50)
    summary: str = Field(default="", max_length=500)

    @field_validator("file_content")
    @classmethod
    def must_look_like_jest(cls, v: str) -> str:
        if "describe(" not in v or "supertest" not in v:
            raise ValueError("file_content must be a Jest + supertest unit test")
        if "require(" not in v or "src/app" not in v:
            raise ValueError("file_content must import app from src")
        return v


class AgentResponse(BaseModel):
    """Wrapper for JSON schema v1 output."""

    output_format: str = Field(default="json_schema_v1")
    generated_test: GeneratedUnitTest
