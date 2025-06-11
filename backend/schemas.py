# schemas.py
from pydantic import BaseModel
from typing import List, Optional

class ChatResponse(BaseModel):
    response: str
    options: List[str] = []
    requires_input: Optional[str] = None
    conversation_state: Optional[str] = None

class ChatMessage(BaseModel):
    message: str
    session_id: str
