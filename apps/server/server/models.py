from typing import List, Literal, Optional, Dict, Any
from pydantic import BaseModel, Field


class Persona(BaseModel):
    id: str
    displayName: str
    goals: List[str] = Field(default_factory=list)
    guardrails: Dict[str, Any] = Field(default_factory=dict)
    ragNamespaces: List[str] = Field(default_factory=list)
    tools: List[str] = Field(default_factory=list)
    ui: Dict[str, List[str]] = Field(default_factory=lambda: {"modules": []})
    voice: Dict[str, Any] = Field(default_factory=dict)


class Message(BaseModel):
    role: Literal['user', 'assistant', 'system']
    content: str


class OrchestrateReq(BaseModel):
    persona: str
    user_id: str
    messages: List[Message]
    tools_hint: Optional[List[str]] = None


class ToolEvent(BaseModel):
    name: str
    input: Dict[str, Any]
    output: Dict[str, Any]


class Reply(BaseModel):
    text: str
    media: Optional[Dict[str, Any]] = None


class Offer(BaseModel):
    id: str
    name: str
    copy: str
    cta: Dict[str, Any]


class OrchestrateRes(BaseModel):
    reply: Reply
    offers: List[Offer]
    tool_events: List[ToolEvent]
