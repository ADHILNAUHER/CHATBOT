from fastapi import APIRouter
from fastapi.responses import StreamingResponse  # Added for streaming
from src.handlers.chat_handler import (
    chat_agent_handler,
    get_all_threads_handler,
    chat_history_handler,
)

# Note: We removed the ChatAgentState return type hint here because
# the endpoint now returns a stream of text, not a single state object.

router = APIRouter()


@router.post("/chat/{thread_id}")
async def chat_agent_route(thread_id: str, message: str):
    """
    Calls the streaming handler and returns a StreamingResponse.
    """
    # We call the async generator handler
    generator = chat_agent_handler(thread_id=thread_id, message=message)

    # Return the stream with a plain text media type
    return StreamingResponse(generator, media_type="text/plain")


@router.get("/chat/threads")
def get_all_threads() -> list[str | None]:
    return get_all_threads_handler()


@router.get("/chat/history/{thread_id}")
def get_chat_history(thread_id: str):
    return chat_history_handler(thread_id=thread_id)
