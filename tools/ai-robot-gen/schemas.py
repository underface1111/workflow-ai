"""Pydantic contract for AI Robot E2E Agent (Bước D)."""

from pydantic import BaseModel, Field, field_validator


class GeneratedRobotSuite(BaseModel):
    ticket_id: str = Field(..., min_length=1, max_length=64)
    file_name: str = Field(..., pattern=r"^[a-z0-9-]+\.robot$")
    file_content: str = Field(..., min_length=80)
    summary: str = Field(default="", max_length=500)

    @field_validator("file_content")
    @classmethod
    def must_look_like_robot(cls, v: str) -> str:
        if "*** Test Cases ***" not in v:
            raise ValueError("file_content must be a Robot Framework suite")
        if "api_keywords.robot" not in v:
            raise ValueError("file_content must resource-import api_keywords.robot")
        if "generated" not in v.lower():
            raise ValueError("file_content must include generated tag")
        return v


class RobotAgentResponse(BaseModel):
    output_format: str = Field(default="json_schema_v1")
    generated_suite: GeneratedRobotSuite
