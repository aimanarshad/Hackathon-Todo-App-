from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import Optional
from datetime import datetime
import logging

from database import get_session
from conversation_models import (
    Conversation, Message, MessageCreate, MessageResponse, MessagePublic
)
from agents.gemini_agent import get_gemini_agent


def get_db():
    """Wrapper for getting database session for chat router"""
    for session in get_session():
        yield session

router = APIRouter(prefix="/api", tags=["chat"])


@router.post("/chat", response_model=MessageResponse)
async def chat_endpoint(
    message_data: MessageCreate,
    db: Session = Depends(get_db)
):
    """
    Main chat endpoint that processes user messages and returns AI responses
    """
    try:
        # Get the gemini agent instance
        agent = get_gemini_agent()

        # If no conversation_id provided, create a new conversation
        if not message_data.conversation_id:
            conversation = Conversation(
                user_id=1,  # Using dummy user_id for now as per spec
                title="New Conversation"
            )
            db.add(conversation)
            db.commit()
            db.refresh(conversation)
            conversation_id = conversation.id
        else:
            conversation_id = message_data.conversation_id

            # Verify conversation exists
            conversation = db.query(Conversation).filter(
                Conversation.id == conversation_id
            ).first()
            if not conversation:
                raise HTTPException(status_code=404, detail="Conversation not found")

        # Create user message entry
        user_message = Message(
            conversation_id=conversation_id,
            role="user",
            content=message_data.message
        )
        db.add(user_message)
        db.commit()
        db.refresh(user_message)

        # Get conversation history for context
        conversation_history = db.query(Message).filter(
            Message.conversation_id == conversation_id
        ).order_by(Message.timestamp).all()

        # Format history for the agent (only include content and role)
        formatted_history = [
            {"role": msg.role, "content": msg.content}
            for msg in conversation_history[:-1]  # Exclude the current message
        ]

        # Process the message with the agent
        result = agent.chat(message_data.message, formatted_history)

        # Create assistant response message
        assistant_message = Message(
            conversation_id=conversation_id,
            role="assistant",
            content=result["response"]
        )
        db.add(assistant_message)
        db.commit()
        db.refresh(assistant_message)

        # Update conversation timestamp
        conversation.updated_at = datetime.utcnow()
        db.commit()

        # Prepare response
        response = MessageResponse(
            response=result["response"],
            conversation_id=conversation_id,
            message_id=assistant_message.id,
            tool_calls=result.get("tool_calls")
        )

        return response

    except Exception as e:
        logging.error(f"Chat endpoint error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


@router.get("/chat/conversations/{conversation_id}", response_model=list[MessagePublic])
async def get_conversation_history(
    conversation_id: int,
    db: Session = Depends(get_db)
):
    """
    Retrieve the history of messages for a specific conversation
    """
    conversation = db.query(Conversation).filter(
        Conversation.id == conversation_id
    ).first()

    if not conversation:
        raise HTTPException(status_code=404, detail="Conversation not found")

    messages = db.query(Message).filter(
        Message.conversation_id == conversation_id
    ).order_by(Message.timestamp).all()

    return messages


@router.get("/chat/conversations", response_model=list)
async def list_user_conversations(
    user_id: Optional[int] = 1,  # Using dummy user_id for now
    db: Session = Depends(get_db)
):
    """
    List all conversations for a user
    """
    conversations = db.query(Conversation).filter(
        Conversation.user_id == user_id
    ).order_by(Conversation.created_at.desc()).all()

    return [
        {
            "id": conv.id,
            "title": conv.title,
            "created_at": conv.created_at,
            "updated_at": conv.updated_at
        }
        for conv in conversations
    ]