from fastapi import APIRouter, Depends, HTTPException
from backend.models import ChatMessage, ChatResponse
from backend.auth import get_current_user_id
from backend.ai_chatbot import chatbot

router = APIRouter(prefix="/api/chat", tags=["AI Chatbot"])

@router.post("/", response_model=ChatResponse)
async def chat_with_ai(
    message: ChatMessage,
    user_id: str = Depends(get_current_user_id)
):
    """Chat with the AI academic planning assistant"""
    try:
        response = await chatbot.chat(user_id, message.message)
        return ChatResponse(response=response)
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error processing chat request: {str(e)}"
        )
