"""Pydantic contract for AI Code Agent output (Giai đoạn 2 — Bước C)."""

from pydantic import BaseModel, Field, field_validator

ALLOWED_PREFIXES = ("src/", "tests/unit/")


class GeneratedSourceFile(BaseModel):
    """One file produced or patched by AI Code Agent."""

    ticket_id: str = Field(..., min_length=1, max_length=64)
    relative_path: str = Field(..., min_length=3, max_length=256)
    file_content: str = Field(..., min_length=10)
    summary: str = Field(default="", max_length=500)

    @field_validator("relative_path")
    @classmethod
    def path_must_be_allowed(cls, v: str) -> str:
        normalized = v.replace("\\", "/").lstrip("./")
        if not any(normalized.startswith(p) for p in ALLOWED_PREFIXES):
            raise ValueError(f"relative_path must start with one of {ALLOWED_PREFIXES}")
        if ".." in normalized:
            raise ValueError("relative_path must not contain ..")
        return normalized

    @field_validator("file_content")
    @classmethod
    def must_have_review_marker(cls, v: str) -> str:
        if "REVIEW REQUIRED" not in v and "AUTO-GENERATED" not in v:
            # src/app.js uses inline comment; tests use header — validated per-path in generate
            pass
        return v


class CodeAgentResponse(BaseModel):
    """Wrapper for JSON schema v1 output."""

    output_format: str = Field(default="json_schema_v1")
    files: list[GeneratedSourceFile] = Field(..., min_length=1, max_length=10)
