from sqlmodel import SQLModel, Field, Relationship
from datetime import datetime
from typing import TYPE_CHECKING, Optional
from pydantic import BaseModel

if TYPE_CHECKING:
    from models import Task  # Assuming existing Task model


class ConversationBase(SQLModel):
    user_id: int
    title: Optional[str] = None


class Conversation(ConversationBase, table=True):
    __tablename__ = "conversations"

    id: int = Field(default=None, primary_key=True)
    user_id: int = Field(index=True)
    title: Optional[str] = Field(default=None)
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)

    # Relationship to messages
    messages: list["Message"] = Relationship(
        back_populates="conversation",
        cascade_delete=True
    )


class ConversationPublic(ConversationBase):
    id: int
    created_at: datetime
    updated_at: datetime


class MessageBase(SQLModel):
    conversation_id: int
    role: str  # "user" or "assistant"
    content: str
    message_metadata: Optional[str] = None  # Changed from dict to str for JSON serialization and renamed to avoid conflicts


class Message(MessageBase, table=True):
    __tablename__ = "messages"

    id: int = Field(default=None, primary_key=True)
    conversation_id: int = Field(foreign_key="conversations.id", index=True)
    role: str = Field()  # Removed check constraint as it's not supported
    content: str = Field()
    timestamp: datetime = Field(default_factory=datetime.now)
    message_metadata: Optional[str] = Field(default=None)  # Changed from dict to str for JSON serialization and renamed to avoid conflicts

    # Relationship to conversation
    conversation: Conversation = Relationship(back_populates="messages")


class MessagePublic(MessageBase):
    id: int
    timestamp: datetime


class MessageCreate(BaseModel):
    conversation_id: Optional[int] = None
    message: str


class MessageResponse(BaseModel):
    response: str
    conversation_id: int
    message_id: int
    tool_calls: Optional[list] = None